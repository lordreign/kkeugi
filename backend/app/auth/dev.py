"""Dev-only auth endpoint — bypass Google verify for local dev/testing.

Only mounted when ENVIRONMENT == 'development' or 'test'.
NEVER enable in production — config.py raises if ENVIRONMENT='production' and
this router is mounted.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.routes import TokenPair, _issue_pair
from app.config import get_settings
from app.db.session import get_db
from app.users.models import User

router = APIRouter(prefix="/v1/auth/dev", tags=["auth-dev"])


class DevLoginRequest(BaseModel):
    email: EmailStr
    name: str | None = None


@router.post("/login", response_model=TokenPair)
async def dev_login(
    body: DevLoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> TokenPair:
    """Create or fetch a user by email, return JWT pair.

    Local dev only. Skips Google verify entirely.
    """
    settings = get_settings()
    if settings.environment == "production":
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    fake_sub = f"dev-{body.email}"
    result = await db.execute(select(User).where(User.google_sub == fake_sub))
    user = result.scalar_one_or_none()

    if user is not None and user.deleted_at is not None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "account deleted")

    if user is None:
        user = User(
            google_sub=fake_sub,
            email=body.email,
            display_name=body.name or body.email.split("@")[0],
            tier="free",
        )
        db.add(user)
        await db.flush()

    return await _issue_pair(db, user, request)
