from datetime import datetime, timezone
from typing import Optional, Literal
from pydantic import BaseModel, Field, model_validator


class UserEventListFilter(BaseModel):
    limit: int = Field(ge=1, le=100)
    offset: int = Field(ge=0)
    sort_by: Literal["starts_at", "ends_at"] = Field(default="starts_at")
    order: Literal["asc", "desc"] = Field(default="asc")


class EventCreate(BaseModel):
    title: str
    description: str = Field(max_length=2048)
    starts_at: datetime
    ends_at: datetime
    country_id: int
    region_id: Optional[int] = None

    @model_validator(mode="after")
    def check_dates(cls, values):
        current_time = datetime.now(timezone.utc)
        if values.starts_at >= values.ends_at:
            raise ValueError("'starts_at' must be earlier than 'ends_at'.")
        if values.starts_at <= current_time:
            raise ValueError("'starts_at' must be in the future.")
        return values


class EventUpdate(BaseModel):
    title: str
    description: str = Field(max_length=2048)
    starts_at: datetime
    ends_at: datetime
    country_id: int
    region_id: Optional[int] = None

    @model_validator(mode="after")
    def check_dates(cls, values):
        current_time = datetime.now(timezone.utc)
        if values.starts_at >= values.ends_at:
            raise ValueError("'starts_at' must be earlier than 'ends_at'.")
        if values.starts_at <= current_time:
            raise ValueError("'starts_at' must be in the future.")
        return values
