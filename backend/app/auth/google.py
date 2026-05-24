from dataclasses import dataclass

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from app.config import get_settings


@dataclass
class GoogleIdentity:
    sub: str
    email: str
    name: str | None
    email_verified: bool


class GoogleVerifyError(Exception):
    pass


def verify_google_id_token(token: str) -> GoogleIdentity:
    settings = get_settings()
    try:
        info = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.google_client_id,
        )
    except ValueError as e:
        raise GoogleVerifyError(f"invalid id_token: {e}") from e

    if not info.get("email_verified", False):
        raise GoogleVerifyError("email not verified by Google")

    return GoogleIdentity(
        sub=info["sub"],
        email=info["email"],
        name=info.get("name"),
        email_verified=True,
    )
