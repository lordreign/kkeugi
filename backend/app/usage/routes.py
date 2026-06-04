from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.deps import get_current_user
from app.usage.models import UsageEvent, UsageEventDedupe
from app.usage.schemas import (
    CategoryStat,
    DayStat,
    MonthLoss,
    TodayStats,
    UsageBatchRequest,
    UsageBatchResponse,
    UsageEventIn,
    WeekStats,
)
from app.users.models import User

# V1 EXECUTION PLAN §2 — hourly_value 미설정 시 default 시급(원).
_DEFAULT_HOURLY_VALUE = 30_000

router = APIRouter(prefix="/v1/usage", tags=["usage"])


def _in_work_hours(occurred_at: datetime, user: User, tz: ZoneInfo) -> bool:
    """occurred_at(UTC)가 user 작업 시간대 [start, end)에 속하는지."""
    if user.work_start_hour is None or user.work_end_hour is None:
        return False
    local = occurred_at.astimezone(tz)
    start, end = user.work_start_hour, user.work_end_hour
    if start <= end:
        return start <= local.hour < end
    # 자정을 넘는 작업 시간대 (예: 22~6시)
    return local.hour >= start or local.hour < end


@router.post("/batch", response_model=UsageBatchResponse)
async def batch(
    body: UsageBatchRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UsageBatchResponse:
    if not body.events:
        return UsageBatchResponse(accepted=[], duplicate=[])

    # 같은 배치 안 중복 client_event_id 정리 (먼저 온 것 우선)
    unique: dict = {}
    for e in body.events:
        unique.setdefault(e.client_event_id, e)
    events: list[UsageEventIn] = list(unique.values())

    # 멱등 게이트: dedupe INSERT ... ON CONFLICT DO NOTHING RETURNING
    dedupe_stmt = (
        pg_insert(UsageEventDedupe)
        .values([{"user_id": user.id, "client_event_id": e.client_event_id} for e in events])
        .on_conflict_do_nothing(index_elements=["user_id", "client_event_id"])
        .returning(UsageEventDedupe.client_event_id)
    )
    accepted_ids = set((await db.execute(dedupe_stmt)).scalars().all())

    tz = ZoneInfo(user.timezone)
    new_rows = [e for e in events if e.client_event_id in accepted_ids]
    if new_rows:
        db.add_all(
            UsageEvent(
                user_id=user.id,
                package_name=e.package_name,
                category=e.category,
                duration_seconds=e.duration_seconds,
                occurred_at=e.occurred_at,
                in_work_hours=_in_work_hours(e.occurred_at, user, tz),
                source=e.source,
                client_event_id=e.client_event_id,
            )
            for e in new_rows
        )
    await db.commit()

    duplicate = [e.client_event_id for e in events if e.client_event_id not in accepted_ids]
    return UsageBatchResponse(accepted=list(accepted_ids), duplicate=duplicate)


def _day_start_utc(now: datetime, tz: ZoneInfo, days_ago: int = 0) -> datetime:
    """user tz 기준 (오늘-days_ago) 00:00을 UTC로."""
    local = now.astimezone(tz) - timedelta(days=days_ago)
    local_midnight = local.replace(hour=0, minute=0, second=0, microsecond=0)
    return local_midnight.astimezone(UTC)


@router.get("/stats/today", response_model=TodayStats)
async def stats_today(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TodayStats:
    tz = ZoneInfo(user.timezone)
    now = datetime.now(UTC)
    start = _day_start_utc(now, tz)

    rows = (
        await db.execute(
            select(
                UsageEvent.category,
                func.sum(UsageEvent.duration_seconds),
                func.sum(UsageEvent.duration_seconds).filter(
                    UsageEvent.in_work_hours.is_(True),
                ),
            )
            .where(UsageEvent.user_id == user.id, UsageEvent.occurred_at >= start)
            .group_by(UsageEvent.category),
        )
    ).all()

    by_category = [
        CategoryStat(category=cat, minutes=round((secs or 0) / 60)) for cat, secs, _ in rows
    ]
    by_category.sort(key=lambda c: c.minutes, reverse=True)
    total = sum((secs or 0) for _, secs, _ in rows)
    in_work = sum((w or 0) for _, _, w in rows)

    return TodayStats(
        date=now.astimezone(tz).strftime("%Y-%m-%d"),
        total_minutes=round(total / 60),
        in_work_minutes=round(in_work / 60),
        by_category=by_category,
    )


@router.get("/stats/week", response_model=WeekStats)
async def stats_week(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> WeekStats:
    tz = ZoneInfo(user.timezone)
    now = datetime.now(UTC)
    start = _day_start_utc(now, tz, days_ago=6)  # 오늘 포함 7일

    # 카테고리별 합계
    cat_rows = (
        await db.execute(
            select(UsageEvent.category, func.sum(UsageEvent.duration_seconds))
            .where(UsageEvent.user_id == user.id, UsageEvent.occurred_at >= start)
            .group_by(UsageEvent.category),
        )
    ).all()
    by_category = [
        CategoryStat(category=cat, minutes=round((secs or 0) / 60)) for cat, secs in cat_rows
    ]
    by_category.sort(key=lambda c: c.minutes, reverse=True)
    total = sum((secs or 0) for _, secs in cat_rows)

    # 일자별 합계 (user tz 기준 날짜로 버킷팅)
    day_expr = func.to_char(
        func.timezone(user.timezone, UsageEvent.occurred_at), "YYYY-MM-DD",
    )
    day_rows = (
        await db.execute(
            select(day_expr.label("d"), func.sum(UsageEvent.duration_seconds))
            .where(UsageEvent.user_id == user.id, UsageEvent.occurred_at >= start)
            .group_by(day_expr)
            .order_by(day_expr),
        )
    ).all()
    day_map = {d: round((secs or 0) / 60) for d, secs in day_rows}

    by_day = []
    for i in range(6, -1, -1):
        d = (now.astimezone(tz) - timedelta(days=i)).strftime("%Y-%m-%d")
        by_day.append(DayStat(date=d, total_minutes=day_map.get(d, 0)))

    return WeekStats(
        total_minutes=round(total / 60),
        by_category=by_category,
        by_day=by_day,
    )


@router.get("/stats/month-loss", response_model=MonthLoss)
async def stats_month_loss(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MonthLoss:
    """월초(user tz) ~ 현재 누적 손실. paywall 직전 표시용.

    무료/유료 모두 호출 가능. paywall 진입 trigger 에서만 노출(홈 상시 X).
    """
    tz = ZoneInfo(user.timezone)
    now = datetime.now(UTC)
    local_now = now.astimezone(tz)
    local_month_start = local_now.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0,
    )
    start = local_month_start.astimezone(UTC)

    secs = (
        await db.execute(
            select(func.coalesce(func.sum(UsageEvent.duration_seconds), 0)).where(
                UsageEvent.user_id == user.id, UsageEvent.occurred_at >= start,
            ),
        )
    ).scalar_one()

    minutes = round((secs or 0) / 60)
    hourly = user.hourly_value or _DEFAULT_HOURLY_VALUE
    # loss_won = minutes × (hourly / 60). 분당 ₩.
    loss_won = round(minutes * hourly / 60)
    return MonthLoss(minutes=minutes, loss_won=loss_won, hourly_value=hourly)
