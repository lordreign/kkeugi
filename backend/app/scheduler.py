"""APScheduler — 주간 리플렉션 + 일일 정리 + 월 파티션.

FastAPI lifespan에서 start/stop. test 환경에서는 시작하지 않는다.
"""
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.db.session import async_session_maker
from app.reports.service import run_weekly_reflection
from app.usage.partitions import ensure_next_month_partition
from app.users.cleanup import hard_delete_expired_accounts

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone="Asia/Seoul")


async def _weekly_reflection_job() -> None:
    async with async_session_maker() as db:
        n = await run_weekly_reflection(db)
        logger.info("[cron] weekly reflection: %d reports", n)
        # TODO(W6 Step 3): dispatch to channels (FCM/email/telegram)


async def _daily_cleanup_job() -> None:
    async with async_session_maker() as db:
        n = await hard_delete_expired_accounts(db)
        logger.info("[cron] hard-deleted %d expired accounts", n)


async def _partition_job() -> None:
    async with async_session_maker() as db:
        name = await ensure_next_month_partition(db)
        logger.info("[cron] partition ensured: %s", name)


def start_scheduler() -> None:
    if scheduler.running:
        return
    # 일요일 22:00 KST — 주간 회고
    scheduler.add_job(
        _weekly_reflection_job,
        CronTrigger(day_of_week="sun", hour=22, minute=0),
        id="weekly_reflection",
        replace_existing=True,
    )
    # 매일 03:00 — 만료 계정 hard delete (PIPA 30일)
    scheduler.add_job(
        _daily_cleanup_job,
        CronTrigger(hour=3, minute=0),
        id="daily_cleanup",
        replace_existing=True,
    )
    # 매월 1일 03:30 — 다음 달 파티션
    scheduler.add_job(
        _partition_job,
        CronTrigger(day=1, hour=3, minute=30),
        id="create_partition",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("scheduler started (Asia/Seoul)")


def shutdown_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
