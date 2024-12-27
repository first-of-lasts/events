from events.domain.models.user import UserDM
from events.application.interfaces import user_interface


class GetCurrentUserInteractor:
    def __init__(
            self,
            user_gateway: user_interface.UserReader,
    ) -> None:
        self._user_gateway = user_gateway

    async def __call__(self, email: str, language: str) -> UserDM:
        return await self._user_gateway.get_by_email(email, language)


class UpdateCurrentUserInteractor:
    def __init__(
            self,
            user_gateway: user_interface.UserUpdater,
    ):
        self._user_gateway = user_gateway

    async def __call__(self, email: str, update_data: dict):
        await self._user_gateway.update(email, update_data)
