import gettext

from events.domain.exceptions.user import UserNotFoundError
from events.domain.models.user import UserDM
from events.application.interfaces import user_interface


class GetUserInteractor:
    def __init__(
            self,
            user_gateway: user_interface.UserReader,
            translations: dict[str, gettext.GNUTranslations],
    ) -> None:
        self._user_gateway = user_gateway
        self._translations = translations

    async def __call__(self, email: str, language: str) -> UserDM:
        user = await self._user_gateway.get_by_email(email, language)
        return user


class UpdateUserInteractor:
    def __init__(
            self,
            user_gateway: user_interface.UserUpdater,
    ):
        self._user_gateway = user_gateway

    async def __call__(self, email: str, update_data: dict):
        await self._user_gateway.update(email, update_data)
