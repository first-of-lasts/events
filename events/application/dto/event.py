from typing import Optional

from pydantic import BaseModel


class NewEventDTO(BaseModel):
    title: str
    description: str
    country_id: int
    region_id: Optional[int] = None
