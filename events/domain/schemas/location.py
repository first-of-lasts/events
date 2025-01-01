from pydantic import BaseModel


class CountryList(BaseModel):
    id: int
    code: str
    name: str


class RegionList(BaseModel):
    id: int
    name: str
