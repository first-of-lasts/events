from abc import abstractmethod
from typing import Protocol, List, Optional

from events.application.schemas.responses import location_response


class CountryReader(Protocol):
    @abstractmethod
    async def exists_country_by_id(self, country_id: int) -> bool:
        ...

    @abstractmethod
    async def get_countries_list(
            self,
            language: str
    ) -> List[location_response.CountryList]:
        ...


class RegionReader(Protocol):
    @abstractmethod
    async def get_region_country_id(self, region_id: int) -> Optional[int]:
        ...

    @abstractmethod
    async def get_regions_list(
            self,
            country_id: int,
            language: str,
    ) -> List[location_response.RegionList]:
        ...


class LocationGatewayInterface(CountryReader, RegionReader, Protocol):
    pass
