from typing import Optional, Literal

from pydantic import BaseModel, Field


class NewEventDTO(BaseModel):
    title: str
    description: str = Field(max_length=2048)
    country_id: int
    region_id: Optional[int] = None


class UpdateEventDTO(BaseModel):
    title: str
    description: str = Field(max_length=2048)
    country_id: int
    region_id: Optional[int] = None


class ListUserEventsDTO(BaseModel):
    limit: int = Field(ge=1, le=100)
    offset: int = Field(ge=0)
    sort_by: Literal["created_at", "updated_at"] = Field(default="created_at")
    order: Literal["asc", "desc"] = Field(default="asc")
