import uuid
from datetime import UTC, datetime, timedelta

import pytest_asyncio


@pytest_asyncio.fixture
async def auth(client):
    """dev login → (client에 헤더 적용된 토큰, user dict) 반환."""
    r = await client.post("/v1/auth/dev/login", json={"email": "u@test.com", "name": "U"})
    data = r.json()
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    return headers, data["user"]


def _event(occurred_at: datetime, category="sns", seconds=600, pkg="com.x", cid=None):
    return {
        "client_event_id": str(cid or uuid.uuid4()),
        "package_name": pkg,
        "category": category,
        "duration_seconds": seconds,
        "occurred_at": occurred_at.isoformat(),
        "source": "usagestats",
    }


async def test_batch_requires_auth(client):
    r = await client.post("/v1/usage/batch", json={"events": []})
    assert r.status_code in (401, 403)


async def test_batch_empty(client, auth):
    headers, _ = auth
    r = await client.post("/v1/usage/batch", json={"events": []}, headers=headers)
    assert r.status_code == 200
    assert r.json() == {"accepted": [], "duplicate": []}


async def test_batch_inserts_and_is_idempotent(client, auth):
    headers, _ = auth
    now = datetime.now(UTC)
    cid = uuid.uuid4()
    ev = _event(now, cid=cid)

    r1 = await client.post("/v1/usage/batch", json={"events": [ev]}, headers=headers)
    assert r1.status_code == 200
    assert r1.json()["accepted"] == [str(cid)]
    assert r1.json()["duplicate"] == []

    # 같은 client_event_id 재전송 → duplicate, 저장 안 함
    r2 = await client.post("/v1/usage/batch", json={"events": [ev]}, headers=headers)
    assert r2.json()["accepted"] == []
    assert r2.json()["duplicate"] == [str(cid)]


async def test_batch_dedupes_within_same_request(client, auth):
    headers, _ = auth
    now = datetime.now(UTC)
    cid = uuid.uuid4()
    ev = _event(now, cid=cid)
    r = await client.post("/v1/usage/batch", json={"events": [ev, ev]}, headers=headers)
    assert r.status_code == 200
    assert r.json()["accepted"] == [str(cid)]


async def test_batch_rejects_nonpositive_duration(client, auth):
    headers, _ = auth
    ev = _event(datetime.now(UTC), seconds=0)
    r = await client.post("/v1/usage/batch", json={"events": [ev]}, headers=headers)
    assert r.status_code == 422


async def test_batch_rejects_bad_category(client, auth):
    headers, _ = auth
    ev = _event(datetime.now(UTC), category="email")
    r = await client.post("/v1/usage/batch", json={"events": [ev]}, headers=headers)
    assert r.status_code == 422


async def test_stats_today(client, auth):
    headers, _ = auth
    now = datetime.now(UTC)
    events = [
        _event(now, category="sns", seconds=1080),      # 18분
        _event(now, category="shorts", seconds=840),     # 14분
        _event(now, category="webtoon", seconds=660),    # 11분
    ]
    await client.post("/v1/usage/batch", json={"events": events}, headers=headers)

    r = await client.get("/v1/usage/stats/today", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["total_minutes"] == 43
    cats = {c["category"]: c["minutes"] for c in data["by_category"]}
    assert cats == {"sns": 18, "shorts": 14, "webtoon": 11}
    # 가장 큰 카테고리가 먼저 (내림차순)
    assert data["by_category"][0]["category"] == "sns"


async def test_stats_today_by_app(client, auth):
    headers, _ = auth
    now = datetime.now(UTC)
    events = [
        _event(now, category="sns", seconds=1200, pkg="com.instagram.android"),   # 20분
        _event(now, category="shorts", seconds=600, pkg="com.google.android.youtube"),  # 10분
        _event(now, category="other", seconds=300, pkg="com.toss.app"),            # 5분
    ]
    await client.post("/v1/usage/batch", json={"events": events}, headers=headers)

    r = await client.get("/v1/usage/stats/today", headers=headers)
    assert r.status_code == 200
    by_app = r.json()["by_app"]
    # 분 내림차순 + package_name 그대로
    assert [a["package_name"] for a in by_app] == [
        "com.instagram.android",
        "com.google.android.youtube",
        "com.toss.app",
    ]
    assert by_app[0]["minutes"] == 20


async def test_stats_today_excludes_other_days(client, auth):
    headers, _ = auth
    now = datetime.now(UTC)
    old = now - timedelta(days=3)
    await client.post(
        "/v1/usage/batch",
        json={"events": [_event(now, seconds=600), _event(old, seconds=600)]},
        headers=headers,
    )
    r = await client.get("/v1/usage/stats/today", headers=headers)
    assert r.json()["total_minutes"] == 10  # 오늘 것만


async def test_stats_week(client, auth):
    headers, _ = auth
    now = datetime.now(UTC)
    await client.post(
        "/v1/usage/batch",
        json={
            "events": [
                _event(now, category="sns", seconds=600),
                _event(now - timedelta(days=2), category="game", seconds=1200),
            ],
        },
        headers=headers,
    )
    r = await client.get("/v1/usage/stats/week", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["total_minutes"] == 30
    assert len(data["by_day"]) == 7


async def test_stats_month_loss_default_hourly(client, auth):
    """V1 EXECUTION PLAN §2: 시급 미설정 시 default ₩30,000/h."""
    headers, _ = auth
    now = datetime.now(UTC)
    # 60분 (3600초) 흩어짐
    await client.post(
        "/v1/usage/batch",
        json={"events": [_event(now, category="sns", seconds=3600)]},
        headers=headers,
    )
    r = await client.get("/v1/usage/stats/month-loss", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["minutes"] == 60
    assert data["hourly_value"] == 30000
    # 60분 × ₩30,000/60 = ₩30,000
    assert data["loss_won"] == 30000


async def test_stats_month_loss_with_user_hourly(client, auth):
    """사용자가 시급 설정 시 그 값 사용."""
    headers, _ = auth
    # 시급 ₩50,000 설정
    await client.patch("/v1/me", json={"hourly_value": 50000}, headers=headers)
    now = datetime.now(UTC)
    # 30분 (1800초)
    await client.post(
        "/v1/usage/batch",
        json={"events": [_event(now, category="sns", seconds=1800)]},
        headers=headers,
    )
    r = await client.get("/v1/usage/stats/month-loss", headers=headers)
    data = r.json()
    assert data["minutes"] == 30
    assert data["hourly_value"] == 50000
    # 30분 × ₩50,000/60 = ₩25,000
    assert data["loss_won"] == 25000


async def test_stats_month_loss_empty(client, auth):
    """이번 달 데이터 없으면 0."""
    headers, _ = auth
    r = await client.get("/v1/usage/stats/month-loss", headers=headers)
    data = r.json()
    assert data["minutes"] == 0
    assert data["loss_won"] == 0
