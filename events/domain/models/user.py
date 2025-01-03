from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class UserDM:
    id: Optional[int] = None
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_verified: Optional[bool] = None
    is_blacklisted: Optional[bool] = None
    country_id: Optional[int] = None
    region_id: Optional[int] = None
