from abc import abstractmethod
from typing import Protocol, List

from events.domain.models.country import CountryDM
from events.domain.models.region import RegionDM


class CountryReader(Protocol):
    @abstractmethod
    async def get_country_list(self, language: str) -> List[CountryDM]:
        ...


class RegionReader(Protocol):
    @abstractmethod
    async def get_region_list(self, country_id: int, language: str) -> List[RegionDM]:
        ...