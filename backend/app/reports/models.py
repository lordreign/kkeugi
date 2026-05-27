import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class WeeklyReport(Base):
    """주간 회고 카드 (wedge #1: 시간 빚 환산 AI 리포트).

    (user_id, week_start_date[월요일]) 유니크 — 주당 1장, 재생성 시 upsert.
    """

    __tablename__ = "weekly_reports"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False,
    )
    week_start_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    recovered_minutes: Mapped[int] = mapped_column(Integer, nullable=False)  # 음수=증가
    recovered_won: Mapped[int | None] = mapped_column(Integer, nullable=True)
    llm_card_text: Mapped[str] = mapped_column(Text, nullable=False)
    llm_card_insight: Mapped[str | None] = mapped_column(Text, nullable=True)
    llm_service_used: Mapped[str | None] = mapped_column(String(20), nullable=True)
    any_channel_sent: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("user_id", "week_start_date", name="uq_weekly_reports_user_week"),
        Index("idx_weekly_reports_user_week", "user_id", "week_start_date"),
    )
