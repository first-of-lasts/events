from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class NewEventDTO:
    title: str
    description: str
    country_id: Optional[int] = None
    region_id: Optional[int] = None
