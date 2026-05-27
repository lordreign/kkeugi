"""계정 hard-delete (PIPA 30일 grace).

soft delete(deleted_at 설정) 후 grace_days 경과한 사용자를 영구 삭제한다.
W6 APScheduler에서 일 1회 호출 예정. 그 전까지는 함수 단위로 테스트 가능.
"""

from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.usage.models import UsageEvent, UsageEventDedupe
from app.users.models import User

GRACE_DAYS = 30


async def hard_delete_expired_accounts(
    db: AsyncSession, grace_days: int = GRACE_DAYS,
) -> int:
    """grace_days 지난 soft-deleted 계정을 영구 삭제. 삭제된 사용자 수 반환.

    FK ON DELETE CASCADE 테이블(refresh_tokens·channel_subscriptions·fcm_tokens·
    thresholds·weekly_reports·subscriptions)은 자동 삭제.
    usage_events·usage_event_dedupe는 FK가 없어(파티션 테이블) 수동 삭제.
    """
    cutoff = datetime.now(UTC) - timedelta(days=grace_days)
    ids = (
        await db.execute(
            select(User.id).where(
                User.deleted_at.is_not(None),
                User.deleted_at < cutoff,
            ),
        )
    ).scalars().all()
    if not ids:
        return 0

    await db.execute(delete(UsageEvent).where(UsageEvent.user_id.in_(ids)))
    await db.execute(delete(UsageEventDedupe).where(UsageEventDedupe.user_id.in_(ids)))
    await db.execute(delete(User).where(User.id.in_(ids)))
    await db.commit()
    return len(ids)
