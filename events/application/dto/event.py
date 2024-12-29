from typing import Optional

from pydantic import BaseModel


class NewEventDTO(BaseModel):
    title: str
    description: str
    country_id: Optional[int] = None
    region_id: Optional[int] = None
