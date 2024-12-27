from typing import List

from events.domain.models.country import CountryDM
from events.domain.models.region import RegionDM
from events.application.interfaces import location_interface


class GetCountriesInteractor:
    def __init__(
            self,
            location_gateway: location_interface.CountryReader,
    ) -> None:
        self._location_gateway = location_gateway

    async def __call__(self, language: str) -> List[CountryDM]:
        return await self._location_gateway.get_country_list(language)


class GetRegionsInteractor:
    def __init__(
            self,
            location_gateway: location_interface.RegionReader,
    ) -> None:
        self._location_gateway = location_gateway

    async def __call__(self, country_id: int, language: str) -> List[RegionDM]:
        return await self._location_gateway.get_region_list(country_id, language)
