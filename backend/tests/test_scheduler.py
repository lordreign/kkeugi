import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from app.reports.models import WeeklyReport
from app.reports.service import run_weekly_reflection
from app.usage.models import UsageEvent
from app.users.models import User


async def _make_user(client, email: str) -> uuid.UUID:
    r = await client.post("/v1/auth/dev/login", json={"email": email})
    return uuid.UUID(r.json()["user"]["id"])


def _ev(uid, when, seconds=600):
    return UsageEvent(
        user_id=uid,
        package_name="com.x",
        category="shorts",
        duration_seconds=seconds,
        occurred_at=when,
        client_event_id=uuid.uuid4(),
    )


async def test_reflection_active_users_only(client, db_session):
    now = datetime.now(UTC)
    active = await _make_user(client, "active@test.com")
    inactive = await _make_user(client, "inactive@test.com")
    db_session.add(_ev(active, now))                          # 최근 사용 → active
    db_session.add(_ev(inactive, now - timedelta(days=20)))   # 20일 전 → inactive
    await db_session.commit()

    n = await run_weekly_reflection(db_session)
    assert n == 1

    active_report = (
        await db_session.execute(
            select(WeeklyReport).where(WeeklyReport.user_id == active),
        )
    ).scalar_one_or_none()
    inactive_report = (
        await db_session.execute(
            select(WeeklyReport).where(WeeklyReport.user_id == inactive),
        )
    ).scalar_one_or_none()
    assert active_report is not None
    assert inactive_report is None


async def test_dev_run_weekly_endpoint(client, db_session):
    now = datetime.now(UTC)
    r = await client.post("/v1/auth/dev/login", json={"email": "cron@test.com"})
    data = r.json()
    uid = uuid.UUID(data["user"]["id"])
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    db_session.add(_ev(uid, now))
    await db_session.commit()

    run = await client.post("/v1/reports/dev/run_weekly")
    assert run.status_code == 200
    assert run.json()["generated"] >= 1

    weekly = await client.get("/v1/reports/weekly", headers=headers)
    assert weekly.status_code == 200


async def test_reflection_skips_deleted_users(client, db_session):
    now = datetime.now(UTC)
    uid = await _make_user(client, "del-active@test.com")
    db_session.add(_ev(uid, now))
    u = await db_session.get(User, uid)
    u.deleted_at = now
    await db_session.commit()

    n = await run_weekly_reflection(db_session)
    assert n == 0
