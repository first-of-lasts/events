from typing import Optional
from events.application.interfaces import location_interface
from events.domain.exceptions.location import (
    CountryNotFoundError,
    RegionNotFoundError,
    InvalidRegionError
)


class LocationValidator:
    def __init__(
            self, location_gateway: location_interface.LocationGatewayInterface
    ):
        self._location_gateway = location_gateway

    async def __call__(
        self,
        country_id: Optional[int],
        region_id: Optional[int]
    ) -> None:
        if country_id:
            country_exists = await self._location_gateway.exists_country_by_id(country_id)
            if not country_exists:
                raise CountryNotFoundError("Country does not exist")

            if region_id:
                region_country_id = await self._location_gateway.get_region_country_id(region_id)
                if not region_country_id:
                    raise RegionNotFoundError("Region does not exist")
                if region_country_id != country_id:
                    raise InvalidRegionError("Invalid region")
        else:
            if region_id:
                raise InvalidRegionError("Invalid region")
