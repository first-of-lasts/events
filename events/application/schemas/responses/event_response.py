from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserEventList(BaseModel):
    id: int
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    is_occurred: bool
    country: str
    region: Optional[str] = None
