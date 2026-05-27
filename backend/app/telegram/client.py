import logging

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)

_API = "https://api.telegram.org"


class TelegramNotConfiguredError(RuntimeError):
    """TELEGRAM_BOT_TOKEN 미설정."""


async def send_message(chat_id: str, text: str) -> bool:
    """텔레그램 메시지 발송. 성공 여부 반환.

    bot token만 있으면 로컬에서도 즉시 동작 (public URL·Play Console 무관).
    """
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise TelegramNotConfiguredError("TELEGRAM_BOT_TOKEN not set")

    url = f"{_API}/bot{settings.telegram_bot_token}/sendMessage"
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.post(
                url,
                json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            )
            if resp.status_code != 200:
                logger.warning("telegram send failed %s: %s", resp.status_code, resp.text)
                return False
            return True
        except httpx.HTTPError as e:
            logger.warning("telegram send error: %s", e)
            return False
