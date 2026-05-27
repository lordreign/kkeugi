import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Subscription(Base):
    """결제/구독 (Google Play Billing V1, Toss V2).

    멱등: gp_purchase_token unique — 동일 영수증 재검증 시 중복 생성 방지.
    server-authoritative: kind/amount는 product_id에서 서버가 결정(클라 미신뢰).
    """

    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False,
    )
    source: Mapped[str] = mapped_column(String(20), nullable=False, default="google_play")
    kind: Mapped[str] = mapped_column(String(20), nullable=False)
    gp_purchase_token: Mapped[str | None] = mapped_column(
        String(500), unique=True, nullable=True,
    )
    gp_order_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    gp_product_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    toss_payment_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
    toss_order_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    amount_krw: Mapped[int] = mapped_column(Integer, nullable=False)
    net_krw: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    trial_starts_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )
    refunded_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )
    promo_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    discount_percent: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )

    __table_args__ = (
        CheckConstraint("source IN ('google_play', 'toss')", name="subs_source_check"),
        CheckConstraint(
            "kind IN ('one_time', 'monthly', 'yearly')", name="subs_kind_check",
        ),
        CheckConstraint(
            "status IN ('active', 'in_trial', 'cancelled', 'expired', 'refunded')",
            name="subs_status_check",
        ),
        Index(
            "idx_subscriptions_user_active",
            "user_id",
            postgresql_where="status IN ('active', 'in_trial')",
        ),
        Index("idx_subscriptions_gp_token", "gp_purchase_token"),
    )
