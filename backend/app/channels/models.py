import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    SmallInteger,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

# multi-channel retention (wedge #3). V1: fcm/email/telegram. V1.5: discord/slack.
CHANNELS = ("fcm", "email", "telegram", "discord", "slack")


class ChannelSubscription(Base):
    """사용자별 알림 채널 구독. (user_id, channel) 유니크.

    channel_identifier 의미: telegram=chat_id, email=email 주소, fcm=token 별도 테이블.
    바인딩 전 대기 상태는 channel_identifier='pending:<token>' + subscribed=false.
    """

    __tablename__ = "channel_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    channel: Mapped[str] = mapped_column(String(20), nullable=False)
    channel_identifier: Mapped[str] = mapped_column(String(500), nullable=False)
    subscribed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    preferred_send_hour: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, default=22,
    )
    subscribed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )
    unsubscribed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )
    # 'metadata'는 SQLAlchemy 예약어 → 속성명 meta, 컬럼명 metadata
    meta: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "channel IN ('fcm', 'email', 'telegram', 'discord', 'slack')",
            name="channel_subscriptions_channel_check",
        ),
        UniqueConstraint("user_id", "channel", name="uq_channel_subs_user_channel"),
        Index(
            "idx_channel_subscriptions_active",
            "user_id",
            postgresql_where="subscribed = TRUE",
        ),
    )


class FcmToken(Base):
    """FCM 디바이스 토큰 (사용자당 여러 기기 가능)."""

    __tablename__ = "fcm_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    token: Mapped[str] = mapped_column(String(1024), unique=True, nullable=False)
    device_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )

    __table_args__ = (Index("idx_fcm_tokens_user", "user_id"),)
