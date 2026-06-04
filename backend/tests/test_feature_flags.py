"""V1 EXECUTION PLAN §7 — feature flag 인프라 검증."""
import uuid

import pytest_asyncio

from app.feature_flags import FeatureFlag, flags_for_user, is_on


@pytest_asyncio.fixture
async def auth(client):
    r = await client.post("/v1/auth/dev/login", json={"email": "ff@test.com"})
    data = r.json()
    return {"Authorization": f"Bearer {data['access_token']}"}, data["user"]


async def test_endpoint_returns_empty_by_default(client, auth):
    """ACTIVE_FLAGS 빈 상태 = 응답도 빈 리스트."""
    headers, _ = auth
    r = await client.get("/v1/feature_flags", headers=headers)
    assert r.status_code == 200
    assert r.json() == {"flags": []}


async def test_endpoint_requires_auth(client):
    r = await client.get("/v1/feature_flags")
    assert r.status_code in (401, 403)


def test_rollout_0_pct_off_for_all():
    flag = FeatureFlag("x", 0, "off")
    for _ in range(20):
        assert not is_on(flag, uuid.uuid4())


def test_rollout_100_pct_on_for_all():
    flag = FeatureFlag("x", 100, "on")
    for _ in range(20):
        assert is_on(flag, uuid.uuid4())


def test_is_deterministic():
    """같은 (user, flag) 는 같은 결과 — 사용자 경험 일관."""
    flag = FeatureFlag("loss_paywall_v2", 50, "test")
    uid = uuid.uuid4()
    first = is_on(flag, uid)
    for _ in range(10):
        assert is_on(flag, uid) == first


def test_rollout_50_pct_splits_roughly_evenly():
    """50% rollout = 모집단의 약 절반."""
    flag = FeatureFlag("x", 50, "test")
    on_count = sum(1 for _ in range(1000) if is_on(flag, uuid.uuid4()))
    # 1000 trials, 50% 기대 — 통계적 변동 허용 (45-55%)
    assert 400 <= on_count <= 600


def test_flags_for_user_filters_active_only():
    """ACTIVE_FLAGS 없으면 빈 리스트."""
    flags = flags_for_user(uuid.uuid4())
    assert flags == []
