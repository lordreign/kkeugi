from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.deps import get_current_user
from app.payments.entitlement import get_active_subscription
from app.payments.models import Subscription
from app.payments.products import PRODUCTS, TRIAL_DAYS
from app.payments.schemas import EntitlementOut, SubscriptionOut, VerifyRequest
from app.payments.verifier import get_verifier
from app.users.models import User

router = APIRouter(prefix="/v1/payments", tags=["payments"])


def _to_out(sub: Subscription) -> SubscriptionOut:
    return SubscriptionOut(
        kind=sub.kind,
        status=sub.status,
        product_id=sub.gp_product_id,
        source=sub.source,
        starts_at=sub.starts_at,
        expires_at=sub.expires_at,
    )


@router.post("/verify", response_model=SubscriptionOut)
async def verify_purchase(
    body: VerifyRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SubscriptionOut:
    """영수증 검증 → 구독 생성 + tier 갱신. gp_purchase_token 기준 멱등."""
    if body.source != "google_play":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "unsupported source (V1)")
    product = PRODUCTS.get(body.product_id)
    if product is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "unknown product_id")

    # 멱등: 동일 purchase_token 이미 처리됐으면 그대로 반환
    existing = (
        await db.execute(
            select(Subscription).where(
                Subscription.gp_purchase_token == body.purchase_token,
            ),
        )
    ).scalar_one_or_none()
    if existing is not None:
        return _to_out(existing)

    verified = await get_verifier().verify(body.product_id, body.purchase_token)
    if not verified.valid:
        raise HTTPException(
            status.HTTP_402_PAYMENT_REQUIRED, f"verification failed: {verified.reason}",
        )

    now = datetime.now(UTC)
    is_trial = body.trial and product.kind in ("monthly", "yearly")
    if is_trial:
        sub_status = "in_trial"
        trial_starts = now
        expires = now + timedelta(days=TRIAL_DAYS)
        amount = 0
    else:
        sub_status = "active"
        trial_starts = None
        expires = now + timedelta(days=product.duration_days)
        amount = product.amount_krw

    sub = Subscription(
        user_id=user.id,
        source="google_play",
        kind=product.kind,
        gp_purchase_token=body.purchase_token,
        gp_order_id=verified.order_id,
        gp_product_id=product.product_id,
        amount_krw=amount,
        net_krw=round(amount * 0.7),
        status=sub_status,
        trial_starts_at=trial_starts,
        starts_at=now,
        expires_at=expires,
    )
    db.add(sub)
    user.tier = "one_time" if product.kind == "one_time" else "subscription"
    await db.commit()
    await db.refresh(sub)
    return _to_out(sub)


@router.get("/subscription", response_model=EntitlementOut)
async def subscription_status(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> EntitlementOut:
    sub = await get_active_subscription(db, user.id)
    if sub is None:
        return EntitlementOut(paid=False, in_trial=False)
    return EntitlementOut(
        paid=True,
        in_trial=sub.status == "in_trial",
        kind=sub.kind,
        expires_at=sub.expires_at,
    )
