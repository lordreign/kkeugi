"""주간 회고 카드 생성 — wedge #1.

dev/test 또는 키 미설정: FakeLLM(stats 기반 템플릿, 결정론적).
prod(키 설정): Anthropic Haiku. 톤 = 거울 같은 친구(압박X·비난X·객관O·지속 동기).
"""
import logging
from dataclasses import dataclass

from app.config import get_settings

logger = logging.getLogger(__name__)


@dataclass
class CardContext:
    total_minutes: int
    recovered_minutes: int  # 음수 = 증가
    recovered_won: int | None
    top_category_label: str | None  # 예: "쇼츠"
    peak_label: str | None          # 예: "화요일 오후"


@dataclass
class Card:
    text: str
    insight: str | None
    service_used: str


_SYSTEM = (
    "너는 한국 1인 워커의 '거울 같은 친구'다. 절대 압박하거나 비난하지 않는다. "
    "객관적 사실만 담담히 전하고, 지속 동기를 부드럽게 남긴다. "
    "2~3문장, 존댓말, 이모지 금지."
)


def _won_phrase(won: int | None) -> str:
    if won is None:
        return ""
    if won >= 0:
        return f" 회복한 시간은 약 {won:,}원이에요."
    return f" 늘어난 시간은 약 {abs(won):,}원이에요."


class FakeLLM:
    def generate(self, ctx: CardContext) -> Card:
        if ctx.recovered_minutes >= 0:
            delta = f"지난주보다 {ctx.recovered_minutes}분 줄었어요."
        else:
            delta = f"지난주보다 {abs(ctx.recovered_minutes)}분 늘었어요."
        text = (
            f"이번 주 흩어진 시간은 {ctx.total_minutes}분이에요. "
            f"{delta}{_won_phrase(ctx.recovered_won)}"
        )
        insight = (
            f"{ctx.peak_label}에 가장 많이 흩어졌어요." if ctx.peak_label else None
        )
        return Card(text=text, insight=insight, service_used="fake")


class AnthropicLLM:
    def generate(self, ctx: CardContext) -> Card:
        import anthropic

        settings = get_settings()
        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        prompt = (
            f"이번 주 흩어진 시간 {ctx.total_minutes}분, "
            f"지난주 대비 {ctx.recovered_minutes}분 "
            f"({'감소' if ctx.recovered_minutes >= 0 else '증가'}), "
            f"가장 많은 카테고리 {ctx.top_category_label or '없음'}, "
            f"가장 흩어진 시간대 {ctx.peak_label or '없음'}. "
            "이 사실로 회고 카드 본문(2~3문장)을 써줘."
        )
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system=_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(block.text for block in msg.content if block.type == "text").strip()
        insight = (
            f"{ctx.peak_label}에 가장 많이 흩어졌어요." if ctx.peak_label else None
        )
        return Card(text=text, insight=insight, service_used="anthropic")


def get_llm():
    settings = get_settings()
    if settings.environment in ("development", "test") or not settings.anthropic_api_key:
        return FakeLLM()
    return AnthropicLLM()
