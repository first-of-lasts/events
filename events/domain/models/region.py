from dataclasses import dataclass


@dataclass(slots=True)
class RegionDM:
    id: int
    name: str
