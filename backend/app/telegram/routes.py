import secrets
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.channels.models import ChannelSubscription
from app.config import get_settings
from app.db.session import get_db
from app.deps import get_current_user
from app.telegram.client import TelegramNotConfiguredError, send_message
from app.users.models import User

# 사용자용 (인증 필요)
me_router = APIRouter(prefix="/v1/me/telegram", tags=["telegram"])
# 텔레그램 웹훅 (unversioned, 봇이 호출)
webhook_router = APIRouter(prefix="/webhooks", tags=["telegram"])

_PENDING_PREFIX = "pending:"


class TelegramStatus(BaseModel):
    linked: bool
    subscribed: bool


class LinkTokenResponse(BaseModel):
    link_token: str
    deep_link: str


async def _get_sub(db: AsyncSession, user_id) -> ChannelSubscription | None:
    return (
        await db.execute(
            select(ChannelSubscription).where(
                ChannelSubscription.user_id == user_id,
                ChannelSubscription.channel == "telegram",
            ),
        )
    ).scalar_one_or_none()


@me_router.get("", response_model=TelegramStatus)
async def telegram_status(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TelegramStatus:
    sub = await _get_sub(db, user.id)
    linked = sub is not None and not sub.channel_identifier.startswith(_PENDING_PREFIX)
    return TelegramStatus(linked=linked, subscribed=bool(sub and sub.subscribed))


@me_router.post("/link_token", response_model=LinkTokenResponse)
async def create_link_token(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> LinkTokenResponse:
    """딥링크용 link_token 발급. 사용자가 링크를 열어 /start <token> 보내면 바인딩."""
    token = secrets.token_urlsafe(16)
    sub = await _get_sub(db, user.id)
    if sub is None:
        sub = ChannelSubscription(
            user_id=user.id,
            channel="telegram",
            channel_identifier=f"{_PENDING_PREFIX}{token}",
            subscribed=False,
        )
        db.add(sub)
    else:
        # 재발급 — 기존 row를 pending으로 리셋
        sub.channel_identifier = f"{_PENDING_PREFIX}{token}"
        sub.subscribed = False
        sub.unsubscribed_at = None
    await db.commit()

    settings = get_settings()
    return LinkTokenResponse(
        link_token=token,
        deep_link=f"https://t.me/{settings.telegram_bot_username}?start={token}",
    )


@me_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def unsubscribe(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    sub = await _get_sub(db, user.id)
    if sub is not None and sub.subscribed:
        sub.subscribed = False
        sub.unsubscribed_at = datetime.now(UTC)
        await db.commit()


async def _try_send(chat_id: str, text: str) -> None:
    """dev(토큰 미설정)에서도 바인딩이 깨지지 않도록 발송 실패를 흡수."""
    try:
        await send_message(chat_id, text)
    except TelegramNotConfiguredError:
        pass


@webhook_router.post("/telegram")
async def telegram_webhook(
    update: dict[str, Any],
    db: AsyncSession = Depends(get_db),
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
) -> dict[str, bool]:
    """텔레그램 update 수신. /start <token> → chat_id 바인딩, /stop → 구독 해제.

    prod: setWebhook 시 등록한 secret_token 헤더 검증. dev: secret 미설정이면 skip.
    """
    settings = get_settings()
    if settings.telegram_webhook_secret and (
        x_telegram_bot_api_secret_token != settings.telegram_webhook_secret
    ):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "bad webhook secret")

    message = update.get("message") or update.get("edited_message")
    if not message:
        return {"ok": True}
    text = (message.get("text") or "").strip()
    chat = message.get("chat") or {}
    chat_id = str(chat.get("id", ""))
    if not chat_id:
        return {"ok": True}

    if text.startswith("/start"):
        parts = text.split(maxsplit=1)
        token = parts[1].strip() if len(parts) > 1 else ""
        if token:
            sub = (
                await db.execute(
                    select(ChannelSubscription).where(
                        ChannelSubscription.channel == "telegram",
                        ChannelSubscription.channel_identifier == f"{_PENDING_PREFIX}{token}",
                    ),
                )
            ).scalar_one_or_none()
            if sub is not None:
                sub.channel_identifier = chat_id
                sub.subscribed = True
                sub.subscribed_at = datetime.now(UTC)
                sub.unsubscribed_at = None
                await db.commit()
                await _try_send(
                    chat_id,
                    "끊기와 연결됐어요. 일요일 22:00에 주간 회고 카드를 보내드릴게요.",
                )
                return {"ok": True}
        await _try_send(chat_id, "연결 링크가 만료됐어요. 앱에서 다시 연결해주세요.")
    elif text == "/stop":
        sub = (
            await db.execute(
                select(ChannelSubscription).where(
                    ChannelSubscription.channel == "telegram",
                    ChannelSubscription.channel_identifier == chat_id,
                ),
            )
        ).scalar_one_or_none()
        if sub is not None:
            sub.subscribed = False
            sub.unsubscribed_at = datetime.now(UTC)
            await db.commit()
        await _try_send(chat_id, "알림을 껐어요. 앱에서 언제든 다시 켤 수 있어요.")

    return {"ok": True}
