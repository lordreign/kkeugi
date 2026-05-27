import uuid
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest_asyncio

from app.reports.service import generate_report, week_start_for
from app.usage.models import UsageEvent
from app.users.models import User

KST = ZoneInfo("Asia/Seoul")


@pytest_asyncio.fixture
async def auth(client):
    r = await client.post("/v1/auth/dev/login", json={"email": "rep@test.com", "name": "R"})
    data = r.json()
    return {"Authorization": f"Bearer {data['access_token']}"}, data["user"]


def _ev(uid, when: datetime, seconds: int, category="shorts"):
    return UsageEvent(
        user_id=uid,
        package_name="com.x",
        category=category,
        duration_seconds=seconds,
        occurred_at=when,
        client_event_id=uuid.uuid4(),
    )


async def _seed_and_generate(db, uid, hourly=30000):
    now = datetime.now(UTC)
    db.add(_ev(uid, now, 600))                       # 이번 주 10분
    db.add(_ev(uid, now - timedelta(days=7), 1200))  # 지난 주 20분
    user = await db.get(User, uid)
    user.hourly_value = hourly
    await db.commit()
    monday = week_start_for(now.astimezone(KST).date())
    return await generate_report(db, user, monday)


async def test_generate_report_computes_recovery(client, auth, db_session):
    _, u = auth
    uid = uuid.UUID(u["id"])
    report = await _seed_and_generate(db_session, uid)
    assert report.total_minutes == 10
    assert report.recovered_minutes == 10          # 20 - 10
    assert report.recovered_won == 5000            # 10분 * 30000 / 60
    assert report.llm_card_text
    assert report.llm_service_used == "fake"


async def test_latest_weekly_404_when_none(client, auth):
    headers, _ = auth
    r = await client.get("/v1/reports/weekly", headers=headers)
    assert r.status_code == 404


async def test_latest_weekly_after_generate_free_hides_won(client, auth, db_session):
    headers, u = auth
    await _seed_and_generate(db_session, uuid.UUID(u["id"]))
    r = await client.get("/v1/reports/weekly", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["total_minutes"] == 10
    assert body["card_text"]
    # 무료 사용자 → 매출 환산(recovered_won) 가려짐
    assert body["recovered_won"] is None


async def test_weekly_won_shown_for_paid(client, auth, db_session):
    headers, u = auth
    await _seed_and_generate(db_session, uuid.UUID(u["id"]))
    # 구매 → 유료
    await client.post(
        "/v1/payments/verify",
        json={
            "product_id": "kkeugi.cert",
            "purchase_token": f"tok-{uuid.uuid4()}",
            "source": "google_play",
        },
        headers=headers,
    )
    r = await client.get("/v1/reports/weekly", headers=headers)
    assert r.json()["recovered_won"] == 5000


async def test_reports_list_hides_won_for_free(client, auth, db_session):
    headers, u = auth
    await _seed_and_generate(db_session, uuid.UUID(u["id"]))
    r = await client.get("/v1/reports", headers=headers)
    assert r.status_code == 200
    assert r.json()[0]["recovered_won"] is None


async def test_weekly_by_date_normalizes_to_monday(client, auth, db_session):
    headers, u = auth
    report = await _seed_and_generate(db_session, uuid.UUID(u["id"]))
    monday = report.week_start_date
    # 같은 주의 임의 날짜(수요일)로 조회해도 월요일 카드 반환
    wednesday = monday + timedelta(days=2)
    r = await client.get(f"/v1/reports/weekly/{wednesday.isoformat()}", headers=headers)
    assert r.status_code == 200
    assert r.json()["week_start_date"] == monday.isoformat()


async def test_regenerate_requires_paid(client, auth):
    headers, _ = auth
    r = await client.post("/v1/reports/regenerate", headers=headers)
    assert r.status_code == 402


async def test_regenerate_after_purchase(client, auth):
    headers, _ = auth
    await client.post(
        "/v1/payments/verify",
        json={
            "product_id": "kkeugi.cert",
            "purchase_token": f"tok-{uuid.uuid4()}",
            "source": "google_play",
        },
        headers=headers,
    )
    r = await client.post("/v1/reports/regenerate", headers=headers)
    assert r.status_code == 200
    assert "card_text" in r.json()
