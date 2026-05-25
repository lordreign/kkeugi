import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Category = Literal["sns", "shorts", "game", "webtoon", "other"]
Source = Literal["usagestats", "manual"]


class UsageEventIn(BaseModel):
    client_event_id: uuid.UUID
    package_name: str = Field(min_length=1, max_length=255)
    category: Category
    duration_seconds: int = Field(gt=0)
    occurred_at: datetime
    source: Source = "usagestats"


class UsageBatchRequest(BaseModel):
    # 한 번에 최대 1000건 (ARCHITECTURE §6 sync flow LIMIT 1000)
    events: list[UsageEventIn] = Field(max_length=1000)


class UsageBatchResponse(BaseModel):
    accepted: list[uuid.UUID]   # 신규 저장된 client_event_id
    duplicate: list[uuid.UUID]  # 이미 존재 (멱등 무시)


class CategoryStat(BaseModel):
    category: Category
    minutes: int


class TodayStats(BaseModel):
    date: str                       # YYYY-MM-DD (user tz 기준)
    total_minutes: int
    in_work_minutes: int            # 작업 시간대에 흩어진 시간
    by_category: list[CategoryStat]


class DayStat(BaseModel):
    date: str
    total_minutes: int


class WeekStats(BaseModel):
    total_minutes: int
    by_category: list[CategoryStat]
    by_day: list[DayStat]           # 최근 7일 (오래된→최신)
