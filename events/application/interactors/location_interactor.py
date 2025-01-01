from typing import List

from events.domain.schemas.location import CountryList, RegionList
from events.application.interfaces import location_interface


class ListCountriesInteractor:
    def __init__(
            self,
            location_gateway: location_interface.CountryReader,
    ) -> None:
        self._location_gateway = location_gateway

    async def __call__(self, language: str) -> List[CountryList]:
        countries = await self._location_gateway.get_countries_list(language)
        return countries


class ListRegionsInteractor:
    def __init__(
            self,
            location_gateway: location_interface.RegionReader,
    ) -> None:
        self._location_gateway = location_gateway

    async def __call__(self, country_id: int, language: str) -> List[RegionList]:
        regions = await self._location_gateway.get_regions_list(country_id, language)
        return regions
