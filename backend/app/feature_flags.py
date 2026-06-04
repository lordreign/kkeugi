"""V1 EXECUTION PLAN §7 — feature flag 인프라.

출시 전 인프라 구축. 출시 후 누적 사용자 500명 도달 시점부터
A/B 테스트 즉시 가능하게 하기 위함.

설계 원칙
- 결정론적 bucket 할당: hash(user_id + flag_name) % 100
- 활성 flag 는 코드 상수로 관리 (DB 테이블 X — V1 단순화)
- 응답은 사용자가 "ON" 인 flag 이름 리스트만 반환

추후 확장
- DB 테이블 + admin UI 는 V1.5 검토
- 1차 사용 예시: paywall 카피 A/B (회복 vs 손실 framing)
"""
import hashlib
import uuid
from dataclasses import dataclass

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.deps import get_current_user
from app.users.models import User


@dataclass(frozen=True)
class FeatureFlag:
    """단일 flag 정의.

    rollout_pct: 0-100 — 사용자 중 ON 상태에 들어갈 비율(결정론적).
    description: 무엇을 토글하는지 짧은 설명.
    """

    name: str
    rollout_pct: int
    description: str


# 현재 활성 flag — 출시 시점엔 비어 있음, 출시 후 A/B 시작 시 추가.
ACTIVE_FLAGS: tuple[FeatureFlag, ...] = (
    # 예시 (출시 후 누적 500명 도달 시 활성):
    # FeatureFlag("loss_paywall_v2", 50, "paywall 손실/회복 framing A/B"),
)


def is_on(flag: FeatureFlag, user_id: uuid.UUID) -> bool:
    """사용자가 이 flag 의 ON 그룹에 속하는지(결정론적).

    같은 (user_id, flag.name) 은 항상 같은 결과 → 사용자 경험 일관.
    """
    if flag.rollout_pct <= 0:
        return False
    if flag.rollout_pct >= 100:
        return True
    h = hashlib.sha256(f"{user_id}:{flag.name}".encode()).hexdigest()
    bucket = int(h[:8], 16) % 100
    return bucket < flag.rollout_pct


def flags_for_user(user_id: uuid.UUID) -> list[str]:
    return [f.name for f in ACTIVE_FLAGS if is_on(f, user_id)]


class FeatureFlagsResponse(BaseModel):
    flags: list[str]


router = APIRouter(prefix="/v1/feature_flags", tags=["feature_flags"])


@router.get("", response_model=FeatureFlagsResponse)
async def get_feature_flags(
    user: User = Depends(get_current_user),
) -> FeatureFlagsResponse:
    """현재 사용자가 ON 인 flag 이름 목록."""
    return FeatureFlagsResponse(flags=flags_for_user(user.id))
