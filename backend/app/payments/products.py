"""상품 카탈로그 — server-authoritative. 클라가 보낸 가격/종류 미신뢰.

product_id는 Google Play Console과 1:1 일치 (변경 불가). 가격은 PRD §4/§7 확정.
Google 수수료 30% 흡수 → net = round(amount * 0.7).
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    product_id: str
    kind: str          # one_time | monthly | yearly
    amount_krw: int
    duration_days: int  # one_time은 사실상 영구 → 큰 값

    @property
    def net_krw(self) -> int:
        # Google Play 수수료 30% 흡수
        return round(self.amount_krw * 0.7)


PRODUCTS: dict[str, Product] = {
    "kkeugi.cert": Product("kkeugi.cert", "one_time", 11000, 36500),  # 100년 ≈ 영구
    "kkeugi.monthly": Product("kkeugi.monthly", "monthly", 5900, 30),
    "kkeugi.yearly": Product("kkeugi.yearly", "yearly", 39000, 365),
}

TRIAL_DAYS = 7  # 7일 무료 체험 (구독 상품 offer)
