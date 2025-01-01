from typing import Optional
from pydantic import BaseModel

from events.domain.models.country import CountryDM
from events.domain.models.region import RegionDM


class CurrentUser(BaseModel):
    id: int
    email: str
    username: str
    bio: str
    country: Optional[CountryDM] = None
    region: Optional[RegionDM] = None
