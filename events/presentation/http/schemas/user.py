from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class GetUser(BaseModel):
    email: EmailStr
    username: str
    bio: Optional[str]


class UpdateUser(BaseModel):
    bio: Optional[str] = Field(None, max_length=1024)
    country_id: Optional[int] = None
    region_id: Optional[int] = None
