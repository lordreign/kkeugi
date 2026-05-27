import uuid
from typing import Literal

from pydantic import BaseModel, Field

Category = Literal["sns", "shorts", "game", "webtoon", "other"]


class ThresholdCreate(BaseModel):
    category: Category
    daily_limit_minutes: int = Field(gt=0, le=1440)


class ThresholdUpdate(BaseModel):
    daily_limit_minutes: int | None = Field(default=None, gt=0, le=1440)
    enabled: bool | None = None


class ThresholdOut(BaseModel):
    id: uuid.UUID
    category: str
    daily_limit_minutes: int
    enabled: bool

    model_config = {"from_attributes": True}
