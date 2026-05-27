import pytest_asyncio


@pytest_asyncio.fixture
async def auth(client):
    r = await client.post("/v1/auth/dev/login", json={"email": "t@test.com", "name": "T"})
    data = r.json()
    return {"Authorization": f"Bearer {data['access_token']}"}, data["user"]


def _start_update(chat_id: int, token: str):
    return {
        "update_id": 1,
        "message": {
            "message_id": 1,
            "chat": {"id": chat_id, "type": "private"},
            "text": f"/start {token}",
        },
    }


async def test_status_default_unlinked(client, auth):
    headers, _ = auth
    r = await client.get("/v1/me/telegram", headers=headers)
    assert r.status_code == 200
    assert r.json() == {"linked": False, "subscribed": False}


async def test_link_token_returns_deep_link(client, auth):
    headers, _ = auth
    r = await client.post("/v1/me/telegram/link_token", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["link_token"]
    assert body["deep_link"].startswith("https://t.me/")
    assert body["link_token"] in body["deep_link"]


async def test_webhook_start_binds_and_status_linked(client, auth):
    headers, _ = auth
    token = (await client.post("/v1/me/telegram/link_token", headers=headers)).json()[
        "link_token"
    ]

    # 텔레그램 웹훅으로 /start <token> 수신 → chat_id 바인딩
    r = await client.post("/webhooks/telegram", json=_start_update(99887766, token))
    assert r.status_code == 200
    assert r.json() == {"ok": True}

    status = (await client.get("/v1/me/telegram", headers=headers)).json()
    assert status == {"linked": True, "subscribed": True}


async def test_webhook_unknown_token_no_crash(client, auth):
    r = await client.post("/webhooks/telegram", json=_start_update(1, "bogustoken"))
    assert r.status_code == 200
    assert r.json() == {"ok": True}


async def test_webhook_empty_update_ok(client):
    r = await client.post("/webhooks/telegram", json={"update_id": 5})
    assert r.status_code == 200


async def test_link_token_reissue_resets_pending(client, auth):
    headers, _ = auth
    t1 = (await client.post("/v1/me/telegram/link_token", headers=headers)).json()[
        "link_token"
    ]
    # 한 번 바인딩
    await client.post("/webhooks/telegram", json=_start_update(111, t1))
    # 재발급 → 다시 pending (linked false)
    t2 = (await client.post("/v1/me/telegram/link_token", headers=headers)).json()[
        "link_token"
    ]
    assert t1 != t2
    status = (await client.get("/v1/me/telegram", headers=headers)).json()
    assert status["linked"] is False


async def test_unsubscribe(client, auth):
    headers, _ = auth
    token = (await client.post("/v1/me/telegram/link_token", headers=headers)).json()[
        "link_token"
    ]
    await client.post("/webhooks/telegram", json=_start_update(222, token))

    r = await client.delete("/v1/me/telegram", headers=headers)
    assert r.status_code == 204
    status = (await client.get("/v1/me/telegram", headers=headers)).json()
    # 연결은 유지되지만 구독은 꺼짐
    assert status == {"linked": True, "subscribed": False}


async def test_webhook_stop_unsubscribes(client, auth):
    headers, _ = auth
    token = (await client.post("/v1/me/telegram/link_token", headers=headers)).json()[
        "link_token"
    ]
    await client.post("/webhooks/telegram", json=_start_update(333, token))

    stop = {
        "update_id": 2,
        "message": {"message_id": 2, "chat": {"id": 333, "type": "private"}, "text": "/stop"},
    }
    await client.post("/webhooks/telegram", json=stop)
    status = (await client.get("/v1/me/telegram", headers=headers)).json()
    assert status["subscribed"] is False


async def test_link_requires_auth(client):
    r = await client.post("/v1/me/telegram/link_token")
    assert r.status_code in (401, 403)
