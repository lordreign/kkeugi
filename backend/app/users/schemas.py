import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    display_name: str | None
    tier: str
    hourly_value: int | None
    work_start_hour: int | None
    work_end_hour: int | None
    timezone: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    hourly_value: int | None = None
    work_start_hour: int | None = None
    work_end_hour: int | None = None
    timezone: str | None = None
    display_name: str | None = None
