from datetime import date, datetime

from pydantic import BaseModel


class WeeklyReportOut(BaseModel):
    week_start_date: date
    total_minutes: int
    recovered_minutes: int
    recovered_won: int | None
    card_text: str
    card_insight: str | None
    created_at: datetime

    @classmethod
    def from_model(cls, r, *, show_revenue: bool = True) -> "WeeklyReportOut":
        # 매출 환산(recovered_won)은 유료 전용 — 무료는 null로 가린다.
        return cls(
            week_start_date=r.week_start_date,
            total_minutes=r.total_minutes,
            recovered_minutes=r.recovered_minutes,
            recovered_won=r.recovered_won if show_revenue else None,
            card_text=r.llm_card_text,
            card_insight=r.llm_card_insight,
            created_at=r.created_at,
        )
