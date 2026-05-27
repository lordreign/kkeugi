"""usage_events 월별 파티션 자동 생성 (매월 1일 cron).

prod 전용 — 테스트는 ORM create_all(비파티션)이라 호출하지 않는다.
"""
import logging
from datetime import UTC, datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


def _month_partition_sql(year: int, month: int) -> str:
    ny, nm = (year, month + 1) if month < 12 else (year + 1, 1)
    return (
        f"CREATE TABLE IF NOT EXISTS usage_events_y{year}m{month:02d} "
        f"PARTITION OF usage_events "
        f"FOR VALUES FROM ('{year}-{month:02d}-01') TO ('{ny}-{nm:02d}-01')"
    )


async def ensure_next_month_partition(db: AsyncSession) -> str:
    """다음 달 파티션 생성 (idempotent). 생성한 파티션명 반환."""
    now = datetime.now(UTC)
    y, m = (now.year, now.month + 1) if now.month < 12 else (now.year + 1, 1)
    await db.execute(text(_month_partition_sql(y, m)))
    await db.commit()
    name = f"usage_events_y{y}m{m:02d}"
    logger.info("ensured partition %s", name)
    return name
