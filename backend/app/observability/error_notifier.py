"""백엔드 unhandled 에러를 운영자 Telegram chat 으로 알림 (Sentry 대체).

설계 원칙
- 알림 실패가 본 요청 응답을 막지 않는다 (fire-and-forget, never raise).
- 같은 fingerprint(path+exc_class+msg) 5분 cooldown — spam 방지.
- TELEGRAM_OPS_CHAT_ID 미설정 시 전 흐름 graceful skip.
- 운영자 chat 과 사용자 발송 chat 분리 (사용자에게 stack trace 노출 X).

사용
    from app.observability.error_notifier import notify_exception
    await notify_exception(exc, path="/v1/...", user_email="dev@test.com")

테스트 가능한 순수 함수
- make_fingerprint() — 동일 입력 → 동일 출력
- should_notify(state, fp, now) — cooldown 결정론
"""
from __future__ import annotations

import asyncio
import logging
import traceback
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from app.config import get_settings
from app.telegram.client import TelegramNotConfiguredError, send_message

logger = logging.getLogger(__name__)


def make_fingerprint(path: str, exc: BaseException) -> str:
    """동일 에러 그룹핑 키. 메시지 처음 100자까지 포함(긴 stack 회피)."""
    msg = str(exc)[:100]
    return f"{path}::{type(exc).__name__}::{msg}"


@dataclass
class CooldownState:
    """fingerprint → 마지막 발송 시각. 메모리 dict (프로세스 재시작 시 초기화)."""

    last_sent: dict[str, datetime] = field(default_factory=dict)
    skipped_count: dict[str, int] = field(default_factory=dict)


_state = CooldownState()


def should_notify(
    state: CooldownState,
    fp: str,
    now: datetime,
    cooldown: timedelta,
) -> bool:
    """순수 함수 — 이 fingerprint 를 지금 발송할지 여부.

    side effect: 발송 결정 시 state.last_sent 갱신 / skip 시 skipped_count 증가.
    """
    last = state.last_sent.get(fp)
    if last is None or (now - last) >= cooldown:
        state.last_sent[fp] = now
        state.skipped_count[fp] = 0
        return True
    state.skipped_count[fp] = state.skipped_count.get(fp, 0) + 1
    return False


def format_message(
    *,
    path: str,
    exc: BaseException,
    user_email: str | None = None,
    user_id: str | None = None,
    skipped_since: int = 0,
) -> str:
    """Telegram 발송용 텍스트. 길이 제한(4096자) 대비 trace 최근 5프레임만."""
    tb = traceback.format_exception(type(exc), exc, exc.__traceback__)
    # 마지막 5프레임 + 예외 메시지
    trace_lines = "".join(tb[-6:]).strip()
    # Telegram 4096자 안전
    if len(trace_lines) > 2800:
        trace_lines = trace_lines[:2800] + "\n...(truncated)"

    user_part = ""
    if user_email or user_id:
        user_part = f"\n👤 user: {user_email or '?'} ({(user_id or '?')[:8]}...)"

    skipped_note = ""
    if skipped_since:
        skipped_note = f"\n🔁 같은 에러 {skipped_since}회 cooldown 중"

    now_kst = datetime.now(UTC).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    return (
        f"🚨 끊기 백엔드 에러\n"
        f"📍 {path}\n"
        f"⚠️ {type(exc).__name__}: {str(exc)[:200]}{user_part}\n"
        f"🕒 {now_kst}{skipped_note}\n\n"
        f"```\n{trace_lines}\n```"
    )


async def notify_exception(
    exc: BaseException,
    *,
    path: str,
    user_email: str | None = None,
    user_id: str | None = None,
) -> None:
    """fire-and-forget. 절대 raise 하지 않는다(알림이 응답을 못 막게)."""
    try:
        settings = get_settings()
        ops_chat = settings.telegram_ops_chat_id
        if not ops_chat:
            return  # graceful skip — 운영자 chat 미설정
        if not settings.telegram_bot_token:
            return  # 봇 토큰 미설정

        fp = make_fingerprint(path, exc)
        now = datetime.now(UTC)
        cooldown = timedelta(seconds=settings.error_notifier_cooldown_sec)

        # 발송 결정 (side effect — state mutate)
        if not should_notify(_state, fp, now, cooldown):
            return  # cooldown 중 — 카운트만 증가

        msg = format_message(
            path=path,
            exc=exc,
            user_email=user_email,
            user_id=user_id,
            skipped_since=_state.skipped_count.get(fp, 0),
        )
        await send_message(ops_chat, msg)
    except TelegramNotConfiguredError:
        return  # 정상 fallback
    except Exception as e:
        # 알림 자체가 또 실패 — 로그만 남기고 swallow
        logger.warning("error_notifier failed: %s", e)


def fire_and_forget_notify(
    exc: BaseException,
    *,
    path: str,
    user_email: str | None = None,
    user_id: str | None = None,
) -> None:
    """동기 컨텍스트(scheduler job 등)에서 알림 트리거. event loop 있으면 schedule."""
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(
            notify_exception(
                exc, path=path, user_email=user_email, user_id=user_id,
            ),
        )
    except RuntimeError:
        # 동기 컨텍스트 (테스트 등) — 그냥 swallow
        logger.debug("no event loop; skipping telegram error notify")
