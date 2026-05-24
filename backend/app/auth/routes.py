import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.google import GoogleVerifyError, verify_google_id_token
from app.auth.jwt import (
    TokenError,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.db.session import get_db
from app.users.models import RefreshToken, User
from app.users.schemas import UserOut

router = APIRouter(prefix="/v1/auth", tags=["auth"])


class GoogleLoginRequest(BaseModel):
    id_token: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    user: UserOut


def _client_meta(request: Request) -> tuple[str | None, str | None]:
    ua = request.headers.get("user-agent")
    ip = request.client.host if request.client else None
    return ua, ip


async def _issue_pair(
    db: AsyncSession, user: User, request: Request,
) -> TokenPair:
    jti = uuid.uuid4()
    refresh, expires_at = create_refresh_token(user.id, jti)
    access = create_access_token(user.id)
    ua, ip = _client_meta(request)

    db.add(
        RefreshToken(
            jti=jti,
            user_id=user.id,
            expires_at=expires_at,
            user_agent=ua,
            ip_address=ip,
        ),
    )
    await db.commit()

    return TokenPair(access_token=access, refresh_token=refresh, user=UserOut.model_validate(user))


@router.post("/google", response_model=TokenPair)
async def login_google(
    body: GoogleLoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> TokenPair:
    try:
        identity = verify_google_id_token(body.id_token)
    except GoogleVerifyError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e)) from e

    result = await db.execute(select(User).where(User.google_sub == identity.sub))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            google_sub=identity.sub,
            email=identity.email,
            display_name=identity.name,
            tier="free",
        )
        db.add(user)
        await db.flush()
    else:
        if user.deleted_at is not None:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "account deleted")
        if user.email != identity.email or user.display_name != identity.name:
            user.email = identity.email
            user.display_name = identity.name

    return await _issue_pair(db, user, request)


@router.post("/refresh", response_model=TokenPair)
async def refresh(
    body: RefreshRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> TokenPair:
    try:
        payload = decode_token(body.refresh_token, expected_type="refresh")
    except TokenError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e)) from e

    jti = uuid.UUID(payload["jti"])
    user_id = uuid.UUID(payload["sub"])

    rt = await db.get(RefreshToken, jti)
    if rt is None or rt.revoked_at is not None:
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
            ),
        )
        for compromised in result.scalars():
            compromised.revoked_at = datetime.now(UTC)
        await db.commit()
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "refresh token reuse detected")

    rt.revoked_at = datetime.now(UTC)

    user = await db.get(User, user_id)
    if user is None or user.deleted_at is not None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "user not found")

    new_jti = uuid.uuid4()
    new_refresh, expires_at = create_refresh_token(user.id, new_jti)
    new_access = create_access_token(user.id)
    ua, ip = _client_meta(request)

    db.add(
        RefreshToken(
            jti=new_jti,
            user_id=user.id,
            expires_at=expires_at,
            user_agent=ua,
            ip_address=ip,
        ),
    )
    await db.flush()  # insert new row before FK reference
    rt.rotated_to = new_jti
    await db.commit()

    return TokenPair(
        access_token=new_access, refresh_token=new_refresh, user=UserOut.model_validate(user),
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(body: RefreshRequest, db: AsyncSession = Depends(get_db)) -> None:
    try:
        payload = decode_token(body.refresh_token, expected_type="refresh")
    except TokenError:
        return

    jti = uuid.UUID(payload["jti"])
    rt = await db.get(RefreshToken, jti)
    if rt is not None and rt.revoked_at is None:
        rt.revoked_at = datetime.now(UTC)
        await db.commit()
