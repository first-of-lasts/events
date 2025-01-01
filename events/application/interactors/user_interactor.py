from events.domain.schemas import user as schemas
from events.domain.exceptions.user import UserNotFoundError
from events.application.interfaces import user_interface
from events.application.services.location_validator import LocationValidator
from events.application.dto import user as user_dto


class GetCurrentUserInteractor:
    def __init__(
            self,
            user_gateway: user_interface.UserReader,
    ) -> None:
        self._user_gateway = user_gateway

    async def __call__(self, user_email: str, language: str) -> schemas.CurrentUser:
        current_user = await self._user_gateway.get_current_user(email=user_email, language=language)
        if current_user:
            return current_user
        else:
            raise UserNotFoundError("User not found")


class UpdateCurrentUserInteractor:
    def __init__(
            self,
            user_gateway: user_interface.UserUpdater,
            location_validator: LocationValidator,
    ) -> None:
        self._user_gateway = user_gateway
        self._location_validator = location_validator

    async def __call__(self, dto: user_dto.UpdateUserDTO, user_email: str) -> None:
        await self._location_validator(dto.country_id, dto.region_id)
        update_data = dto.model_dump()
        await self._user_gateway.update_user(email=user_email, update_data=update_data)
