"""채널별 발송 — 미설정 시 graceful skip(False 반환, 예외 X).

- email: Mailgun REST (httpx)
- fcm: FCM HTTP v1 API + Firebase 서비스계정 OAuth2 (httpx, firebase-admin 미사용)
- telegram: app.telegram.client.send_message 재사용
"""
import json
import logging

import anyio
import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)

_FCM_SCOPE = "https://www.googleapis.com/auth/firebase.messaging"


async def send_email(to_addr: str, subject: str, html: str) -> bool:
    settings = get_settings()
    if not settings.mailgun_api_key or not settings.mailgun_domain:
        logger.info("mailgun not configured — skip email")
        return False
    url = f"https://api.mailgun.net/v3/{settings.mailgun_domain}/messages"
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                url,
                auth=("api", settings.mailgun_api_key),
                data={
                    "from": settings.mailgun_from,
                    "to": to_addr,
                    "subject": subject,
                    "html": html,
                },
            )
        if resp.status_code == 200:
            return True
        logger.warning("mailgun failed %s: %s", resp.status_code, resp.text[:200])
        return False
    except httpx.HTTPError as e:
        logger.warning("mailgun error: %s", e)
        return False


async def _fcm_access_token(sa_json: str) -> str:
    from google.auth.transport.requests import Request
    from google.oauth2 import service_account

    creds = service_account.Credentials.from_service_account_info(
        json.loads(sa_json), scopes=[_FCM_SCOPE],
    )
    await anyio.to_thread.run_sync(lambda: creds.refresh(Request()))
    return creds.token


async def send_fcm(token: str, title: str, body: str) -> bool:
    settings = get_settings()
    if not settings.fcm_project_id or not settings.fcm_service_account_json:
        logger.info("fcm not configured — skip push")
        return False
    try:
        access = await _fcm_access_token(settings.fcm_service_account_json)
        url = (
            f"https://fcm.googleapis.com/v1/projects/{settings.fcm_project_id}"
            f"/messages:send"
        )
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                url,
                headers={"Authorization": f"Bearer {access}"},
                json={
                    "message": {
                        "token": token,
                        "notification": {"title": title, "body": body},
                    },
                },
            )
        if resp.status_code == 200:
            return True
        logger.warning("fcm failed %s: %s", resp.status_code, resp.text[:200])
        return False
    except (httpx.HTTPError, ValueError) as e:
        logger.warning("fcm error: %s", e)
        return False
