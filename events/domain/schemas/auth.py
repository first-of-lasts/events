from pydantic import BaseModel, Field, EmailStr


class Login(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)


class PasswordReset(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=32)


class CreateTokenPair(BaseModel):
    refresh_token: str