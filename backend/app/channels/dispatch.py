"""주간 리포트 → 구독 채널 발송. any_channel_sent 기록."""
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.channels.models import ChannelSubscription, FcmToken
from app.channels.senders import send_email, send_fcm
from app.reports.models import WeeklyReport
from app.telegram.client import TelegramNotConfiguredError, send_message
from app.users.models import User

logger = logging.getLogger(__name__)


def _card_text(report: WeeklyReport) -> str:
    text = report.llm_card_text
    if report.llm_card_insight:
        text += f"\n\n{report.llm_card_insight}"
    return text


def _card_html(report: WeeklyReport) -> str:
    insight = f"<p>{report.llm_card_insight}</p>" if report.llm_card_insight else ""
    return f"<h2>이번 주 회고</h2><p>{report.llm_card_text}</p>{insight}"


async def _send_telegram(chat_id: str, text: str) -> bool:
    if chat_id.startswith("pending:"):
        return False
    try:
        return await send_message(chat_id, text)
    except TelegramNotConfiguredError:
        return False


async def _send_fcm_to_user(db: AsyncSession, user_id, title: str, body: str) -> bool:
    tokens = (
        await db.execute(select(FcmToken.token).where(FcmToken.user_id == user_id))
    ).scalars().all()
    sent = False
    for token in tokens:
        if await send_fcm(token, title, body):
            sent = True
    return sent


async def dispatch_report(db: AsyncSession, user: User, report: WeeklyReport) -> bool:
    """구독 중인 모든 채널로 발송. 하나라도 성공하면 any_channel_sent=True."""
    subs = (
        await db.execute(
            select(ChannelSubscription).where(
                ChannelSubscription.user_id == user.id,
                ChannelSubscription.subscribed.is_(True),
            ),
        )
    ).scalars().all()

    text = _card_text(report)
    sent_any = False
    for sub in subs:
        if sub.channel == "telegram":
            ok = await _send_telegram(sub.channel_identifier, text)
        elif sub.channel == "email":
            ok = await send_email(
                sub.channel_identifier, "이번 주 회고 카드", _card_html(report),
            )
        elif sub.channel == "fcm":
            ok = await _send_fcm_to_user(
                db, user.id, "주간 회고가 도착했어요", report.llm_card_text,
            )
        else:
            ok = False
        sent_any = sent_any or ok

    report.any_channel_sent = sent_any
    await db.commit()
    return sent_any
