from typing import Optional

from events.domain.models.user import UserDM
from events.domain.exceptions.user import UserNotFoundError
from events.domain.exceptions.country import CountryNotFoundError
from events.domain.exceptions.region import RegionNotFoundError, InvalidRegionError
from events.application.interfaces import user_interface, location_interface
from events.application.dto import user as user_dto


class GetCurrentUserInteractor:
    def __init__(
            self,
            user_gateway: user_interface.UserReader,
    ) -> None:
        self._user_gateway = user_gateway

    async def __call__(self, email: str, language: str) -> UserDM:
        current_user = await self._user_gateway.get_by_email_with_details(email=email, language=language)
        if current_user:
            return current_user
        else:
            raise UserNotFoundError("User not found")


class UpdateCurrentUserInteractor:
    def __init__(
            self,
            user_gateway: user_interface.UserUpdater,
            location_gateway: location_interface.CountryReader and location_interface.RegionReader,
    ):
        self._user_gateway = user_gateway
        self._location_gateway = location_gateway

    async def __call__(self, dto: user_dto.UpdateUserDTO, email: str):
        locations_valid = await self._locations_valid(dto.country_id, dto.region_id)
        if locations_valid:
            update_values = dto.model_dump()
            if update_values:
                await self._user_gateway.update(email=email, update_data=update_values)

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
