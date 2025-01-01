from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from events.domain.models.country import CountryDM
from events.domain.models.region import RegionDM


@dataclass(slots=True)
class EventDM:
    title: str
    description: str
    id: Optional[int] = None
    user_id: Optional[int] = None
    country_id: Optional[int] = None
    region_id: Optional[int] = None
    country: Optional[CountryDM] = None
    region: Optional[RegionDM] = None
