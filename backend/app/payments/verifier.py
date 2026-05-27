"""영수증 검증 추상화 — dev login 패턴을 결제에 적용.

dev/test: FakeVerifier(토큰 형식만 보고 통과) → Play Console 없이 전 플로우 검증.
prod: GooglePlayVerifier(Google Play Developer API) — Step 6 실기기에서 검증.
"""
import json
import logging
from dataclasses import dataclass

import anyio
import httpx

from app.config import get_settings
from app.payments.products import PRODUCTS

logger = logging.getLogger(__name__)

_ANDROID_PUBLISHER = "https://androidpublisher.googleapis.com/androidpublisher/v3"
_SCOPE = "https://www.googleapis.com/auth/androidpublisher"


@dataclass
class VerifiedPurchase:
    valid: bool
    order_id: str
    reason: str = ""


class Verifier:
    async def verify(self, product_id: str, purchase_token: str) -> VerifiedPurchase:
        raise NotImplementedError


class FakeVerifier(Verifier):
    """dev/test 전용 — 비어있지 않은 토큰이면 통과. 실제 Google 검증 없음."""

    async def verify(self, product_id: str, purchase_token: str) -> VerifiedPurchase:
        if not purchase_token:
            return VerifiedPurchase(valid=False, order_id="", reason="empty token")
        return VerifiedPurchase(valid=True, order_id=f"FAKE-{purchase_token[:24]}")


async def _access_token(sa_json: str) -> str:
    """서비스 계정 JSON → androidpublisher OAuth2 access token (refresh는 thread)."""
    from google.auth.transport.requests import Request
    from google.oauth2 import service_account

    info = json.loads(sa_json)
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=[_SCOPE],
    )
    await anyio.to_thread.run_sync(lambda: creds.refresh(Request()))
    return creds.token


class GooglePlayVerifier(Verifier):
    """prod — Google Play Developer API(androidpublisher)로 purchase_token 검증.

    one_time: purchases.products.get → purchaseState == 0(구매완료).
    subscription: purchases.subscriptionsv2.get → subscriptionState ACTIVE/GRACE.
    실동작 검증은 Step 6(실기기 + 라이선스 테스터).
    """

    async def verify(self, product_id: str, purchase_token: str) -> VerifiedPurchase:
        settings = get_settings()
        if not settings.google_play_service_account_json:
            raise RuntimeError("GOOGLE_PLAY_SERVICE_ACCOUNT_JSON not configured")
        pkg = settings.google_play_package_name
        product = PRODUCTS.get(product_id)
        token = await _access_token(settings.google_play_service_account_json)
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient(timeout=15) as client:
            if product is not None and product.kind == "one_time":
                url = (
                    f"{_ANDROID_PUBLISHER}/applications/{pkg}"
                    f"/purchases/products/{product_id}/tokens/{purchase_token}"
                )
                resp = await client.get(url, headers=headers)
                if resp.status_code != 200:
                    return VerifiedPurchase(False, "", f"http {resp.status_code}")
                data = resp.json()
                ok = data.get("purchaseState") == 0  # 0 = Purchased
                return VerifiedPurchase(ok, data.get("orderId", ""), "" if ok else "not purchased")

            # 구독 (월/연)
            url = (
                f"{_ANDROID_PUBLISHER}/applications/{pkg}"
                f"/purchases/subscriptionsv2/tokens/{purchase_token}"
            )
            resp = await client.get(url, headers=headers)
            if resp.status_code != 200:
                return VerifiedPurchase(False, "", f"http {resp.status_code}")
            data = resp.json()
            state = data.get("subscriptionState", "")
            ok = state in (
                "SUBSCRIPTION_STATE_ACTIVE",
                "SUBSCRIPTION_STATE_IN_GRACE_PERIOD",
            )
            return VerifiedPurchase(ok, data.get("latestOrderId", ""), state)


def get_verifier() -> Verifier:
    settings = get_settings()
    if settings.environment in ("development", "test"):
        return FakeVerifier()
    return GooglePlayVerifier()
