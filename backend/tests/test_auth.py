async def test_google_login_creates_user(client, fake_google_identity):
    r = await client.post("/v1/auth/google", json={"id_token": "alice"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == "user-alice@example.com"
    assert data["user"]["tier"] == "free"


async def test_google_login_idempotent(client, fake_google_identity):
    r1 = await client.post("/v1/auth/google", json={"id_token": "bob"})
    r2 = await client.post("/v1/auth/google", json={"id_token": "bob"})
    assert r1.json()["user"]["id"] == r2.json()["user"]["id"]


async def test_refresh_rotation(client, fake_google_identity):
    r = await client.post("/v1/auth/google", json={"id_token": "carol"})
    refresh = r.json()["refresh_token"]

    r2 = await client.post("/v1/auth/refresh", json={"refresh_token": refresh})
    assert r2.status_code == 200
    new_refresh = r2.json()["refresh_token"]
    assert new_refresh != refresh

    # old refresh token now revoked, reuse triggers full revocation
    r3 = await client.post("/v1/auth/refresh", json={"refresh_token": refresh})
    assert r3.status_code == 401

    # the newly issued refresh token is also revoked (reuse detection cascade)
    r4 = await client.post("/v1/auth/refresh", json={"refresh_token": new_refresh})
    assert r4.status_code == 401


async def test_logout_invalidates_refresh(client, fake_google_identity):
    r = await client.post("/v1/auth/google", json={"id_token": "dan"})
    refresh = r.json()["refresh_token"]

    r2 = await client.post("/v1/auth/logout", json={"refresh_token": refresh})
    assert r2.status_code == 204

    r3 = await client.post("/v1/auth/refresh", json={"refresh_token": refresh})
    assert r3.status_code == 401


async def test_invalid_id_token_rejected(client, monkeypatch):
    from app.auth.google import GoogleVerifyError

    def _raise(token: str):
        raise GoogleVerifyError("bad token")

    monkeypatch.setattr("app.auth.routes.verify_google_id_token", _raise)
    r = await client.post("/v1/auth/google", json={"id_token": "garbage"})
    assert r.status_code == 401


async def test_me_requires_auth(client):
    r = await client.get("/v1/me")
    assert r.status_code in (401, 403)  # HTTPBearer rejects missing creds


async def test_me_returns_current_user(client, fake_google_identity):
    r = await client.post("/v1/auth/google", json={"id_token": "eve"})
    access = r.json()["access_token"]
    r2 = await client.get("/v1/me", headers={"Authorization": f"Bearer {access}"})
    assert r2.status_code == 200
    assert r2.json()["email"] == "user-eve@example.com"


async def test_me_patch_updates_hourly_value(client, fake_google_identity):
    r = await client.post("/v1/auth/google", json={"id_token": "frank"})
    access = r.json()["access_token"]
    r2 = await client.patch(
        "/v1/me",
        json={"hourly_value": 50000},
        headers={"Authorization": f"Bearer {access}"},
    )
    assert r2.status_code == 200
    assert r2.json()["hourly_value"] == 50000
