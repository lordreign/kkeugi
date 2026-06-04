import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.deps import get_current_user
from app.payments.entitlement import get_active_subscription
from app.thresholds.models import Threshold
from app.thresholds.schemas import ThresholdCreate, ThresholdOut, ThresholdUpdate
from app.users.models import User

router = APIRouter(prefix="/v1/thresholds", tags=["thresholds"])

# V1 EXECUTION PLAN §1 — 무료 사용자는 한도 1개까지, 2개 이상부터 유료.
FREE_THRESHOLD_LIMIT = 1


async def _owned(db: AsyncSession, threshold_id: uuid.UUID, user_id) -> Threshold:
    t = await db.get(Threshold, threshold_id)
    if t is None or t.user_id != user_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "threshold not found")
    return t


@router.get("", response_model=list[ThresholdOut])
async def list_thresholds(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Threshold]:
    return list(
        (
            await db.execute(
                select(Threshold)
                .where(Threshold.user_id == user.id)
                .order_by(Threshold.category),
            )
        ).scalars().all(),
    )


@router.post("", response_model=ThresholdOut, status_code=status.HTTP_201_CREATED)
async def create_threshold(
    body: ThresholdCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Threshold:
    # V1 EXECUTION PLAN §1: 무료는 1개까지, 2개째부터 paid 필요.
    count = (
        await db.execute(
            select(func.count(Threshold.id)).where(Threshold.user_id == user.id),
        )
    ).scalar_one()
    if count >= FREE_THRESHOLD_LIMIT:
        sub = await get_active_subscription(db, user.id)
        if sub is None:
            raise HTTPException(
                status.HTTP_402_PAYMENT_REQUIRED,
                f"free tier allows {FREE_THRESHOLD_LIMIT} threshold; upgrade for more",
            )
    exists = (
        await db.execute(
            select(Threshold).where(
                Threshold.user_id == user.id, Threshold.category == body.category,
            ),
        )
    ).scalar_one_or_none()
    if exists is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "category threshold exists")
    t = Threshold(
        user_id=user.id,
        category=body.category,
        daily_limit_minutes=body.daily_limit_minutes,
    )
    db.add(t)
    await db.commit()
    await db.refresh(t)
    return t


@router.patch("/{threshold_id}", response_model=ThresholdOut)
async def update_threshold(
    threshold_id: uuid.UUID,
    body: ThresholdUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Threshold:
    t = await _owned(db, threshold_id, user.id)
    data = body.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(t, k, v)
    await db.commit()
    await db.refresh(t)
    return t


@router.delete("/{threshold_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_threshold(
    threshold_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    t = await _owned(db, threshold_id, user.id)
    await db.delete(t)
    await db.commit()
