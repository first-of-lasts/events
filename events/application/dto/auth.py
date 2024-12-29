from pydantic import BaseModel, Field, EmailStr


class NewUserDTO(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=8, max_length=32)
