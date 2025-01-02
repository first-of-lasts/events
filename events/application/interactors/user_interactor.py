from events.domain.exceptions.user import UserNotFoundError
from events.application.interfaces import user_interface
from events.application.services.location_validator import LocationValidator
from events.application.schemas.requests import user_request
from events.application.schemas.responses import user_response


class GetCurrentUserInteractor:
    def __init__(
            self,
            user_gateway: user_interface.UserReader,
    ) -> None:
        self._user_gateway = user_gateway

    async def __call__(self, user_id: int, language: str) -> user_response.CurrentUser:
        current_user = await self._user_gateway.get_detailed_user(user_id=user_id, language=language)
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

    async def __call__(self, dto: user_request.CurrentUserUpdate, user_id: int) -> None:
        await self._location_validator(dto.country_id, dto.region_id)
        update_data = dto.model_dump()
        await self._user_gateway.update_user(user_id=user_id, update_data=update_data)
