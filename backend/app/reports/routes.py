from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db.session import get_db
from app.deps import get_current_user
from app.payments.entitlement import get_active_subscription, require_paid
from app.reports.models import WeeklyReport
from app.reports.schemas import WeeklyReportOut
from app.reports.service import generate_report, run_weekly_reflection, week_start_for
from app.users.models import User

router = APIRouter(prefix="/v1/reports", tags=["reports"])


@router.get("", response_model=list[WeeklyReportOut])
async def list_reports(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[WeeklyReportOut]:
    """회고 archive — 최신순 전체 목록."""
    rows = (
        await db.execute(
            select(WeeklyReport)
            .where(WeeklyReport.user_id == user.id)
            .order_by(WeeklyReport.week_start_date.desc()),
        )
    ).scalars().all()
    paid = await get_active_subscription(db, user.id) is not None
    return [WeeklyReportOut.from_model(r, show_revenue=paid) for r in rows]


@router.get("/weekly", response_model=WeeklyReportOut)
async def latest_weekly(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> WeeklyReportOut:
    report = (
        await db.execute(
            select(WeeklyReport)
            .where(WeeklyReport.user_id == user.id)
            .order_by(WeeklyReport.week_start_date.desc()),
        )
    ).scalars().first()
    if report is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "no report yet")
    paid = await get_active_subscription(db, user.id) is not None
    return WeeklyReportOut.from_model(report, show_revenue=paid)


@router.get("/weekly/{week_date}", response_model=WeeklyReportOut)
async def weekly_by_date(
    week_date: date,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> WeeklyReportOut:
    monday = week_start_for(week_date)
    report = (
        await db.execute(
            select(WeeklyReport).where(
                WeeklyReport.user_id == user.id,
                WeeklyReport.week_start_date == monday,
            ),
        )
    ).scalar_one_or_none()
    if report is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "no report for week")
    paid = await get_active_subscription(db, user.id) is not None
    return WeeklyReportOut.from_model(report, show_revenue=paid)


@router.post("/regenerate", response_model=WeeklyReportOut)
async def regenerate(
    user: User = Depends(require_paid),
    db: AsyncSession = Depends(get_db),
) -> WeeklyReportOut:
    """현재 주 리포트 강제 재생성 (유료). Google 정책상 rate-limit은 W7."""
    tz = ZoneInfo(user.timezone)
    monday = week_start_for(datetime.now(UTC).astimezone(tz).date())
    report = await generate_report(db, user, monday)
    return WeeklyReportOut.from_model(report)


@router.post("/dev/run_weekly")
async def dev_run_weekly(
    db: AsyncSession = Depends(get_db),
) -> dict[str, int]:
    """dev 전용 — 주간 리플렉션 배치를 즉시 실행 (cron 검증용)."""
    if get_settings().environment == "production":
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    n = await run_weekly_reflection(db)
    return {"generated": n}
