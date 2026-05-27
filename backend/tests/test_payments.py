import uuid

import pytest_asyncio


@pytest_asyncio.fixture
async def auth(client):
    r = await client.post("/v1/auth/dev/login", json={"email": "pay@test.com", "name": "P"})
    data = r.json()
    return {"Authorization": f"Bearer {data['access_token']}"}, data["user"]


def _verify_body(product_id="kkeugi.cert", token=None, trial=False):
    return {
        "product_id": product_id,
        "purchase_token": token or f"tok-{uuid.uuid4()}",
        "source": "google_play",
        "trial": trial,
    }


async def test_verify_requires_auth(client):
    r = await client.post("/v1/payments/verify", json=_verify_body())
    assert r.status_code in (401, 403)


async def test_verify_unknown_product(client, auth):
    headers, _ = auth
    r = await client.post(
        "/v1/payments/verify", json=_verify_body(product_id="kkeugi.bogus"), headers=headers,
    )
    assert r.status_code == 400


async def test_verify_one_time_sets_tier(client, auth):
    headers, _ = auth
    r = await client.post("/v1/payments/verify", json=_verify_body(), headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["kind"] == "one_time"
    assert body["status"] == "active"
    # tier 갱신 확인
    me = (await client.get("/v1/me", headers=headers)).json()
    assert me["tier"] == "one_time"


async def test_verify_idempotent(client, auth):
    headers, _ = auth
    body = _verify_body(token="dup-token-123")
    r1 = await client.post("/v1/payments/verify", json=body, headers=headers)
    r2 = await client.post("/v1/payments/verify", json=body, headers=headers)
    assert r1.status_code == 200
    assert r2.status_code == 200
    # 동일 결과 (중복 생성 X) — subscription 상태로 확인
    sub = (await client.get("/v1/payments/subscription", headers=headers)).json()
    assert sub["paid"] is True


async def test_verify_monthly_trial(client, auth):
    headers, _ = auth
    r = await client.post(
        "/v1/payments/verify",
        json=_verify_body(product_id="kkeugi.monthly", trial=True),
        headers=headers,
    )
    assert r.status_code == 200
    assert r.json()["status"] == "in_trial"
    me = (await client.get("/v1/me", headers=headers)).json()
    assert me["tier"] == "subscription"


async def test_subscription_status_free_by_default(client, auth):
    headers, _ = auth
    r = await client.get("/v1/payments/subscription", headers=headers)
    assert r.status_code == 200
    assert r.json() == {"paid": False, "in_trial": False, "kind": None, "expires_at": None}


async def test_subscription_status_after_purchase(client, auth):
    headers, _ = auth
    await client.post("/v1/payments/verify", json=_verify_body(), headers=headers)
    r = await client.get("/v1/payments/subscription", headers=headers)
    data = r.json()
    assert data["paid"] is True
    assert data["in_trial"] is False
    assert data["kind"] == "one_time"


async def test_verify_empty_token_rejected(client, auth):
    headers, _ = auth
    body = _verify_body()
    body["purchase_token"] = ""
    r = await client.post("/v1/payments/verify", json=body, headers=headers)
    assert r.status_code == 422  # pydantic min_length
