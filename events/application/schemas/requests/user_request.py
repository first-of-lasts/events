from typing import Optional
from pydantic import BaseModel, field_validator, Field


class CurrentUserUpdate(BaseModel):
    bio: str = Field(None, max_length=1024)
    country_id: int
    region_id: Optional[int] = None

    @field_validator("bio")
    def bio_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Bio must not be empty")
        return v
