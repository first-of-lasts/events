from events.domain.exceptions.user import UserNotFoundError
from events.domain.models.user import UserDM
from events.application.interfaces import user_interface


class GetUserInteractor:
    def __init__(
            self,
            user_gateway: user_interface.UserReader,
    ) -> None:
        self._user_gateway = user_gateway

    async def __call__(self, email: str) -> UserDM:
        return await self._user_gateway.get_by_email(email)


class UpdateUserInteractor:
    def __init__(
            self,
            user_gateway: user_interface.UserUpdater,
    ):
        self._user_gateway = user_gateway

    async def __call__(self, email: str, update_data: dict) -> UserDM:
        return await self._user_gateway.update(email, update_data)
