from typing import Optional

from events.domain.models.event import EventDM
from events.domain.exceptions.country import CountryNotFoundError
from events.domain.exceptions.region import RegionNotFoundError, InvalidRegionError
from events.application.interfaces import event_interface, user_interface, location_interface
from events.application.dto import event as event_dto


class CreateEventInteractor:
    def __init__(
            self,
            event_gateway: event_interface.EventCreator,
            user_gateway: user_interface.UserReader,
            location_gateway: location_interface.CountryReader and location_interface.RegionReader,
    ) -> None:
        self._event_gateway = event_gateway
        self._user_gateway = user_gateway
        self._location_gateway = location_gateway

    async def __call__(self, dto: event_dto.NewEventDTO, email: str) -> None:
        user = await self._user_gateway.get_by_email(email)
        locations_valid = await self._locations_valid(dto.country_id, dto.region_id)
        if locations_valid:
            new_event = EventDM(
                user_id=user.id,
                title=dto.title,
                description=dto.description,
                country_id=dto.country_id,
                region_id=dto.region_id,
            )
            await self._event_gateway.create_event(new_event)

    async def _locations_valid(self, country_id: Optional[int], region_id: Optional[int]) -> bool:
        if not country_id:
            if region_id:
                raise InvalidRegionError("Invalid region")
            else:
                return True
        #
        country_exists = await self._location_gateway.exists_country_by_id(country_id)
        if not country_exists:
            raise CountryNotFoundError("Country does not exist")
        if region_id:
            region = await self._location_gateway.get_region(region_id)
            if not region:
                raise RegionNotFoundError("Region does not exist")
            if region.country_id != country_id:
                raise InvalidRegionError("Invalid region")
        return True
