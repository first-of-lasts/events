from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EvenCreate(BaseModel):
    title: str
    description: str = Field(max_length=2048)
    country_id: Optional[int] = None
    region_id: Optional[int] = None


class EventList(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    country: str
    region: Optional[str] = None
