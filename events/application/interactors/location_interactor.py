from typing import List

from events.application.interfaces import location_interface
from events.application.schemas.responses import location_response


class ListCountriesInteractor:
    def __init__(
            self,
            location_gateway: location_interface.CountryReader,
    ) -> None:
        self._location_gateway = location_gateway

    async def __call__(
            self,
            language: str
    ) -> List[location_response.CountryList]:
        countries = await self._location_gateway.get_countries_list(language)
        return countries


class ListRegionsInteractor:
    def __init__(
            self,
            location_gateway: location_interface.RegionReader,
    ) -> None:
        self._location_gateway = location_gateway

    async def __call__(
            self,
            country_id: int,
            language: str
    ) -> List[location_response.RegionList]:
        regions = await self._location_gateway.get_regions_list(country_id, language)
        return regions
