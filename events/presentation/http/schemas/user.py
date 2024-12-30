from typing import Optional

from pydantic import BaseModel, Field


class Country(BaseModel):
    id: int
    code: str
    name: str


class Region(BaseModel):
    id: int
    name: str


class RetrieveUser(BaseModel):
    id: int
    email: str
    username: str
    bio: Optional[str]
    country: Optional[Country]
    region: Optional[Region]
