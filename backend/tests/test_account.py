import uuid
from datetime import UTC, datetime, timedelta

import pytest_asyncio
from sqlalchemy import func, select

from app.usage.models import UsageEvent
from app.users.cleanup import hard_delete_expired_accounts
from app.users.models import User


@pytest_asyncio.fixture
async def auth(client):
    r = await client.post("/v1/auth/dev/login", json={"email": "del@test.com", "name": "D"})
    data = r.json()
    return {"Authorization": f"Bearer {data['access_token']}"}, data["user"]


async def test_delete_me_soft_deletes_and_blocks(client, auth):
    headers, _ = auth
    r = await client.delete("/v1/me", headers=headers)
    assert r.status_code == 204
    # 같은 토큰으로 즉시 차단
    me = await client.get("/v1/me", headers=headers)
    assert me.status_code == 401


async def test_deleted_user_cannot_relogin(client, auth):
    headers, _ = auth
    await client.delete("/v1/me", headers=headers)
    # 동일 이메일 재로그인 차단 (PIPA grace 동안 부활 방지)
    r = await client.post("/v1/auth/dev/login", json={"email": "del@test.com"})
    assert r.status_code == 403


async def test_hard_delete_skips_within_grace(client, auth, db_session):
    headers, user = auth
    await client.delete("/v1/me", headers=headers)
    # 방금 삭제 → grace 안 → 보존
    n = await hard_delete_expired_accounts(db_session, grace_days=30)
    assert n == 0
    still = await db_session.get(User, uuid.UUID(user["id"]))
    assert still is not None


async def test_hard_delete_removes_expired_with_data(client, auth, db_session):
    headers, user = auth
    uid = uuid.UUID(user["id"])

    # usage 이벤트 1건 + soft delete 31일 전으로 설정
    db_session.add(
        UsageEvent(
            user_id=uid,
            package_name="com.x",
            category="sns",
            duration_seconds=600,
            occurred_at=datetime.now(UTC),
            client_event_id=uuid.uuid4(),
        ),
    )
    db_user = await db_session.get(User, uid)
    db_user.deleted_at = datetime.now(UTC) - timedelta(days=31)
    await db_session.commit()

    n = await hard_delete_expired_accounts(db_session, grace_days=30)
    assert n == 1
    assert await db_session.get(User, uid) is None
    # FK 없는 usage_events도 함께 제거
    cnt = (
        await db_session.execute(
            select(func.count()).select_from(UsageEvent).where(UsageEvent.user_id == uid),
        )
    ).scalar()
    assert cnt == 0
