from datetime import datetime

from pydantic import BaseModel, Field


class VerifyRequest(BaseModel):
    product_id: str
    purchase_token: str = Field(min_length=1)
    source: str = "google_play"
    trial: bool = False  # 구독 7일 무료 체험으로 시작 여부


class SubscriptionOut(BaseModel):
    kind: str
    status: str
    product_id: str | None
    source: str
    starts_at: datetime
    expires_at: datetime


class EntitlementOut(BaseModel):
    paid: bool
    in_trial: bool
    kind: str | None = None
    expires_at: datetime | None = None
