from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass(slots=True)
class EventDM:
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    category_ids: List[int]
    id: Optional[int] = None
    user_id: Optional[int] = None
    country_id: Optional[int] = None
    region_id: Optional[int] = None
