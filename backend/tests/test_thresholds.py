import uuid

import pytest_asyncio


@pytest_asyncio.fixture
async def auth(client):
    r = await client.post("/v1/auth/dev/login", json={"email": "th@test.com"})
    data = r.json()
    return {"Authorization": f"Bearer {data['access_token']}"}, data["user"]


async def _make_paid(client, headers):
    await client.post(
        "/v1/payments/verify",
        json={
            "product_id": "kkeugi.cert",
            "purchase_token": f"tok-{uuid.uuid4()}",
            "source": "google_play",
        },
        headers=headers,
    )


async def test_list_empty(client, auth):
    headers, _ = auth
    r = await client.get("/v1/thresholds", headers=headers)
    assert r.status_code == 200
    assert r.json() == []


async def test_create_first_free_succeeds(client, auth):
    """V1 EXECUTION PLAN §1: 무료 사용자도 1개까지는 생성 가능."""
    headers, _ = auth
    r = await client.post(
        "/v1/thresholds", json={"category": "shorts", "daily_limit_minutes": 30}, headers=headers,
    )
    assert r.status_code == 201
    assert r.json()["category"] == "shorts"


async def test_create_second_requires_paid(client, auth):
    """무료는 1개 한도. 2개째 시도하면 402."""
    headers, _ = auth
    # 1개째 생성 — 무료 OK
    await client.post(
        "/v1/thresholds", json={"category": "shorts", "daily_limit_minutes": 30}, headers=headers,
    )
    # 2개째 — 무료 차단
    r = await client.post(
        "/v1/thresholds", json={"category": "sns", "daily_limit_minutes": 20}, headers=headers,
    )
    assert r.status_code == 402


async def test_create_and_list_when_paid(client, auth):
    headers, _ = auth
    await _make_paid(client, headers)
    # 유료는 여러 개 생성 가능
    r1 = await client.post(
        "/v1/thresholds", json={"category": "shorts", "daily_limit_minutes": 30}, headers=headers,
    )
    assert r1.status_code == 201
    r2 = await client.post(
        "/v1/thresholds", json={"category": "sns", "daily_limit_minutes": 20}, headers=headers,
    )
    assert r2.status_code == 201
    lst = await client.get("/v1/thresholds", headers=headers)
    assert len(lst.json()) == 2


async def test_create_duplicate_category_conflict(client, auth):
    headers, _ = auth
    await _make_paid(client, headers)
    body = {"category": "sns", "daily_limit_minutes": 20}
    await client.post("/v1/thresholds", json=body, headers=headers)
    r2 = await client.post("/v1/thresholds", json=body, headers=headers)
    assert r2.status_code == 409


async def test_create_rejects_bad_category(client, auth):
    headers, _ = auth
    await _make_paid(client, headers)
    r = await client.post(
        "/v1/thresholds", json={"category": "email", "daily_limit_minutes": 30}, headers=headers,
    )
    assert r.status_code == 422


async def test_patch_and_delete(client, auth):
    headers, _ = auth
    await _make_paid(client, headers)
    created = (
        await client.post(
            "/v1/thresholds",
            json={"category": "game", "daily_limit_minutes": 60},
            headers=headers,
        )
    ).json()
    tid = created["id"]

    patched = await client.patch(
        f"/v1/thresholds/{tid}",
        json={"daily_limit_minutes": 15, "enabled": False},
        headers=headers,
    )
    assert patched.status_code == 200
    assert patched.json()["daily_limit_minutes"] == 15
    assert patched.json()["enabled"] is False

    d = await client.delete(f"/v1/thresholds/{tid}", headers=headers)
    assert d.status_code == 204
    assert (await client.get("/v1/thresholds", headers=headers)).json() == []


async def test_patch_other_users_threshold_404(client, auth):
    headers, _ = auth
    await _make_paid(client, headers)
    created = (
        await client.post(
            "/v1/thresholds",
            json={"category": "webtoon", "daily_limit_minutes": 30},
            headers=headers,
        )
    ).json()

    other = await client.post("/v1/auth/dev/login", json={"email": "other-th@test.com"})
    other_headers = {"Authorization": f"Bearer {other.json()['access_token']}"}
    r = await client.patch(
        f"/v1/thresholds/{created['id']}", json={"enabled": False}, headers=other_headers,
    )
    assert r.status_code == 404
