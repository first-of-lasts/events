from dataclasses import dataclass
from typing import Optional

from events.domain.models.country import CountryDM


@dataclass(slots=True)
class UserDM:
    id: Optional[int] = None
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    is_verified: Optional[bool] = None
    is_active: Optional[bool] = None
    country: Optional[CountryDM] = None
