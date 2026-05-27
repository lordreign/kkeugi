"""주간 통계 집계 + 리포트 생성 + 주간 리플렉션 배치."""
import logging
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.reports.llm import CardContext, get_llm
from app.reports.models import WeeklyReport
from app.usage.models import UsageEvent
from app.users.models import User

logger = logging.getLogger(__name__)

_CATEGORY_LABELS = {
    "sns": "SNS", "shorts": "쇼츠", "game": "게임", "webtoon": "웹툰", "other": "기타",
}
ACTIVE_DAYS = 7  # active filter: 지난 7일 usage_events ≥1건
# Postgres extract(dow): 0=일 .. 6=토
_DOW_KO = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"]


@dataclass
class WeekStats:
    total_minutes: int = 0
    by_category: dict[str, int] = field(default_factory=dict)
    top_category: str | None = None
    peak_label: str | None = None


def week_start_for(d: date) -> date:
    """그 주의 월요일."""
    return d - timedelta(days=d.weekday())


def _utc_range(week_start: date, tz: ZoneInfo) -> tuple[datetime, datetime]:
    start_local = datetime.combine(week_start, time.min, tzinfo=tz)
    end_local = start_local + timedelta(days=7)
    return start_local.astimezone(UTC), end_local.astimezone(UTC)


async def compute_week_stats(
    db: AsyncSession, user_id, week_start: date, tz: ZoneInfo,
) -> WeekStats:
    start, end = _utc_range(week_start, tz)
    tz_name = str(tz)

    cat_rows = (
        await db.execute(
            select(UsageEvent.category, func.sum(UsageEvent.duration_seconds))
            .where(
                UsageEvent.user_id == user_id,
                UsageEvent.occurred_at >= start,
                UsageEvent.occurred_at < end,
            )
            .group_by(UsageEvent.category),
        )
    ).all()
    by_category = {cat: round((secs or 0) / 60) for cat, secs in cat_rows}
    total = sum(by_category.values())
    if not by_category:
        return WeekStats()

    top_cat = max(by_category, key=by_category.get)

    # peak: (요일, 오전/오후) 버킷 최대
    local_ts = func.timezone(tz_name, UsageEvent.occurred_at)
    dow = func.extract("dow", local_ts)
    ampm = case((func.extract("hour", local_ts) < 12, "오전"), else_="오후")
    peak_rows = (
        await db.execute(
            select(dow, ampm, func.sum(UsageEvent.duration_seconds))
            .where(
                UsageEvent.user_id == user_id,
                UsageEvent.occurred_at >= start,
                UsageEvent.occurred_at < end,
            )
            .group_by(dow, ampm),
        )
    ).all()
    peak_label = None
    if peak_rows:
        d, ap, _ = max(peak_rows, key=lambda r: r[2] or 0)
        peak_label = f"{_DOW_KO[int(d)]} {ap}"

    return WeekStats(
        total_minutes=total,
        by_category=by_category,
        top_category=_CATEGORY_LABELS.get(top_cat, top_cat),
        peak_label=peak_label,
    )


async def generate_report(
    db: AsyncSession, user: User, week_start: date,
) -> WeeklyReport:
    """해당 주 리포트 생성/갱신 (upsert). 발송은 별도(dispatch)."""
    tz = ZoneInfo(user.timezone)
    stats = await compute_week_stats(db, user.id, week_start, tz)
    prev = await compute_week_stats(db, user.id, week_start - timedelta(days=7), tz)
    recovered = prev.total_minutes - stats.total_minutes
    recovered_won = (
        round(recovered * user.hourly_value / 60) if user.hourly_value else None
    )

    card = get_llm().generate(
        CardContext(
            total_minutes=stats.total_minutes,
            recovered_minutes=recovered,
            recovered_won=recovered_won,
            top_category_label=stats.top_category,
            peak_label=stats.peak_label,
        ),
    )

    existing = (
        await db.execute(
            select(WeeklyReport).where(
                WeeklyReport.user_id == user.id,
                WeeklyReport.week_start_date == week_start,
            ),
        )
    ).scalar_one_or_none()

    if existing is None:
        report = WeeklyReport(user_id=user.id, week_start_date=week_start)
        db.add(report)
    else:
        report = existing

    report.total_minutes = stats.total_minutes
    report.recovered_minutes = recovered
    report.recovered_won = recovered_won
    report.llm_card_text = card.text
    report.llm_card_insight = card.insight
    report.llm_service_used = card.service_used
    await db.commit()
    await db.refresh(report)
    return report


async def active_users(db: AsyncSession) -> list[User]:
    """지난 7일 usage_events ≥1건 + 미삭제 사용자 (active filter)."""
    cutoff = datetime.now(UTC) - timedelta(days=ACTIVE_DAYS)
    recent = (
        select(UsageEvent.user_id).where(UsageEvent.occurred_at >= cutoff).distinct()
    )
    return list(
        (
            await db.execute(
                select(User).where(
                    User.id.in_(recent), User.deleted_at.is_(None),
                ),
            )
        ).scalars().all(),
    )


async def run_weekly_reflection(db: AsyncSession) -> int:
    """active 사용자 전원의 현재 주 리포트 생성 + 구독 채널 발송. 생성 건수 반환."""
    from app.channels.dispatch import dispatch_report

    users = await active_users(db)
    count = 0
    for user in users:
        tz = ZoneInfo(user.timezone)
        monday = week_start_for(datetime.now(UTC).astimezone(tz).date())
        try:
            report = await generate_report(db, user, monday)
            await dispatch_report(db, user, report)
            count += 1
        except Exception:  # noqa: BLE001 — 한 사용자 실패가 배치 전체를 막지 않게
            logger.exception("weekly reflection failed for user %s", user.id)
    return count

