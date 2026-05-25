import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Index,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

# 카테고리 enum (DESIGN/ARCHITECTURE 고정 5종)
CATEGORIES = ("sns", "shorts", "game", "webtoon", "other")
SOURCES = ("usagestats", "manual")


class UsageEvent(Base):
    """앱별 사용 이벤트.

    prod는 occurred_at 기준 monthly RANGE partition (alembic 001에서 raw DDL).
    ORM 모델은 테스트 create_all 및 INSERT용 — PK는 prod와 동일 (id, occurred_at).
    멱등성은 usage_events의 unique가 아닌 usage_event_dedupe 테이블로 보장한다.
    """

    __tablename__ = "usage_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    package_name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(20), nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True, nullable=False,
    )
    in_work_hours: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False,
    )
    source: Mapped[str] = mapped_column(
        String(20), nullable=False, default="usagestats",
    )
    client_event_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )

    __table_args__ = (
        CheckConstraint("duration_seconds > 0", name="usage_events_duration_positive"),
        CheckConstraint(
            "category IN ('sns', 'shorts', 'game', 'webtoon', 'other')",
            name="usage_events_category_check",
        ),
        CheckConstraint(
            "source IN ('usagestats', 'manual')",
            name="usage_events_source_check",
        ),
        Index("idx_usage_events_user_occurred", "user_id", "occurred_at"),
    )


class UsageEventDedupe(Base):
    """멱등성 게이트 (non-partitioned). (user_id, client_event_id) PK.

    batch 수신 시 여기 INSERT … ON CONFLICT DO NOTHING으로 신규/중복을 가른다.
    24h TTL daily cleanup cron으로 정리 (W7 threshold/cleanup 단계).
    """

    __tablename__ = "usage_event_dedupe"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    client_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True,
    )
    inserted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )

    __table_args__ = (
        Index("idx_usage_event_dedupe_inserted_at", "inserted_at"),
    )
