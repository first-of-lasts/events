from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class UserEventList(BaseModel):
    id: int
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    categories: List[str]
    country: str
    region: Optional[str] = None
    is_occurred: bool


class EventDetail(BaseModel):
    pass


class RecommendedEventList(BaseModel):
    id: int
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    categories: List[str]
    country: str
    region: Optional[str] = None


class CategoryList(BaseModel):
    id: int
    name: str
