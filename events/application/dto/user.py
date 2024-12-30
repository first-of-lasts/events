from typing import Optional

from pydantic import BaseModel, Field


class UpdateUserDTO(BaseModel):
    bio: Optional[str] = Field(None, max_length=1024)
    country_id: Optional[int] = None
    region_id: Optional[int] = None
