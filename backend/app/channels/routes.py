from datetime import UTC, datetime

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.channels.models import FcmToken
from app.db.session import get_db
from app.deps import get_current_user
from app.users.models import User

router = APIRouter(prefix="/v1/fcm", tags=["fcm"])


class FcmRegisterRequest(BaseModel):
    token: str = Field(min_length=1, max_length=1024)
    device_id: str | None = None


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
async def register_token(
    body: FcmRegisterRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """FCM 디바이스 토큰 등록/갱신 (token 기준 upsert)."""
    existing = (
        await db.execute(select(FcmToken).where(FcmToken.token == body.token))
    ).scalar_one_or_none()
    if existing is None:
        db.add(FcmToken(user_id=user.id, token=body.token, device_id=body.device_id))
    else:
        existing.user_id = user.id
        existing.device_id = body.device_id
        existing.last_seen_at = datetime.now(UTC)
    await db.commit()
