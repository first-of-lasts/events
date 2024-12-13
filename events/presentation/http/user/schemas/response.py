from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserResponse(BaseModel):
    email: str
    username: str
    bio: Optional[str]
