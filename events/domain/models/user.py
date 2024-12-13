from dataclasses import dataclass, field
from typing import Optional


@dataclass(slots=True)
class UserDM:
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    bio: Optional[str] = field(default="")
    is_verified: Optional[bool] = False
