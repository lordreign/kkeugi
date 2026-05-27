"""구독 자격(entitlement) 판정 — paywall gating의 single source of truth.

users.tier는 편의용 denormalized 값. 실제 권한은 subscriptions에서 계산한다.
"""
from datetime import UTC, datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.deps import get_current_user
from app.payments.models import Subscription
from app.users.models import User


async def get_active_subscription(
    db: AsyncSession, user_id,
) -> Subscription | None:
    """유효한(active/in_trial & 미만료) 구독 1건. 없으면 None."""
    now = datetime.now(UTC)
    return (
        await db.execute(
            select(Subscription)
            .where(
                Subscription.user_id == user_id,
                Subscription.status.in_(("active", "in_trial")),
                Subscription.expires_at > now,
            )
            .order_by(Subscription.expires_at.desc()),
        )
    ).scalars().first()


async def require_paid(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    """유료 기능 gating dependency — 무료 사용자는 402."""
    sub = await get_active_subscription(db, user.id)
    if sub is None:
        raise HTTPException(
            status.HTTP_402_PAYMENT_REQUIRED, "paid subscription required",
        )
    return user
