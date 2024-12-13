from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UpdateUserRequest(BaseModel):
    bio: Optional[str] = Field(None, max_length=1024)
