from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class RegionDM:
    id: int
    country_id: Optional[int] = None
    name: Optional[str] = None
