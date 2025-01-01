from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class RegionDM:
    id: int
    name: Optional[str] = None
