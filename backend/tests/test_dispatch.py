import uuid
from datetime import date

import pytest_asyncio

from app.channels import dispatch as dispatch_mod
from app.channels.dispatch import dispatch_report
from app.channels.models import ChannelSubscription
from app.reports.models import WeeklyReport
from app.users.models import User


@pytest_asyncio.fixture
async def auth(client):
    r = await client.post("/v1/auth/dev/login", json={"email": "disp@test.com"})
    data = r.json()
    return {"Authorization": f"Bearer {data['access_token']}"}, data["user"]


async def _report(db, uid) -> WeeklyReport:
    r = WeeklyReport(
        user_id=uid,
        week_start_date=date(2026, 5, 25),
        total_minutes=30,
        recovered_minutes=10,
        recovered_won=5000,
        llm_card_text="이번 주 30분이 흩어졌어요.",
        llm_card_insight="화요일 오후에 가장 많이 흩어졌어요.",
        llm_service_used="fake",
    )
    db.add(r)
    await db.commit()
    await db.refresh(r)
    return r


async def test_dispatch_graceful_skip_when_unconfigured(client, auth, db_session):
    _, u = auth
    uid = uuid.UUID(u["id"])
    db_session.add(
        ChannelSubscription(
            user_id=uid, channel="telegram", channel_identifier="pending:abc",
            subscribed=True,
        ),
    )
    db_session.add(
        ChannelSubscription(
            user_id=uid, channel="fcm", channel_identifier="device", subscribed=True,
        ),
    )
    await db_session.commit()
    report = await _report(db_session, uid)

    sent = await dispatch_report(db_session, await db_session.get(User, uid), report)
    assert sent is False
    assert report.any_channel_sent is False


async def test_dispatch_records_sent_on_success(client, auth, db_session, monkeypatch):
    _, u = auth
    uid = uuid.UUID(u["id"])
    db_session.add(
        ChannelSubscription(
            user_id=uid, channel="email", channel_identifier="x@test.com", subscribed=True,
        ),
    )
    await db_session.commit()
    report = await _report(db_session, uid)

    async def _fake_email(to_addr, subject, html):
        return True

    monkeypatch.setattr(dispatch_mod, "send_email", _fake_email)

    sent = await dispatch_report(db_session, await db_session.get(User, uid), report)
    assert sent is True
    assert report.any_channel_sent is True


async def test_dispatch_ignores_unsubscribed(client, auth, db_session, monkeypatch):
    _, u = auth
    uid = uuid.UUID(u["id"])
    db_session.add(
        ChannelSubscription(
            user_id=uid, channel="email", channel_identifier="x@test.com", subscribed=False,
        ),
    )
    await db_session.commit()
    report = await _report(db_session, uid)

    async def _fake_email(to_addr, subject, html):
        raise AssertionError("should not send to unsubscribed")

    monkeypatch.setattr(dispatch_mod, "send_email", _fake_email)
    sent = await dispatch_report(db_session, await db_session.get(User, uid), report)
    assert sent is False


async def test_fcm_register(client, auth):
    headers, _ = auth
    r = await client.post(
        "/v1/fcm/register", json={"token": "fcm-tok-1", "device_id": "pixel"}, headers=headers,
    )
    assert r.status_code == 204
    # 동일 토큰 재등록 (upsert) — 충돌 없이 204
    r2 = await client.post("/v1/fcm/register", json={"token": "fcm-tok-1"}, headers=headers)
    assert r2.status_code == 204


async def test_fcm_register_requires_auth(client):
    r = await client.post("/v1/fcm/register", json={"token": "x"})
    assert r.status_code in (401, 403)
