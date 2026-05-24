async def test_dev_login_creates_user(client):
    r = await client.post(
        "/v1/auth/dev/login",
        json={"email": "dev@test.com", "name": "Dev User"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["user"]["email"] == "dev@test.com"
    assert data["user"]["display_name"] == "Dev User"
    assert "access_token" in data
    assert "refresh_token" in data


async def test_dev_login_idempotent(client):
    r1 = await client.post("/v1/auth/dev/login", json={"email": "x@test.com"})
    r2 = await client.post("/v1/auth/dev/login", json={"email": "x@test.com"})
    assert r1.json()["user"]["id"] == r2.json()["user"]["id"]
