from dataclasses import dataclass


@dataclass(slots=True)
class CountryDM:
    id: int
    code: str
    name: str
