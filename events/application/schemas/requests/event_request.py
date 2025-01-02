from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field


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
    country_id: Optional[int] = None
    region_id: Optional[int] = None


class EventUpdate(BaseModel):
    title: str
    description: str = Field(max_length=2048)
    starts_at: datetime
    ends_at: datetime
    country_id: int
    region_id: Optional[int] = None
