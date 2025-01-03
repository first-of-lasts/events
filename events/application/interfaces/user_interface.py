from abc import abstractmethod
from typing import Protocol, Optional

from events.domain.models.user import UserDM
from events.application.schemas.responses import user_response


class UserUpdater(Protocol):
    @abstractmethod
    async def update_user(self, user_id: int, update_data: dict) -> None:
        ...


class UserReader(Protocol):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[UserDM]:
        ...

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[UserDM]:
        ...

    @abstractmethod
    async def get_login_user(self, email: str) -> Optional[UserDM]:
        ...

    @abstractmethod
    async def get_detailed_user(
            self,
            user_id: int,
            language: str
    ) -> Optional[user_response.CurrentUser]:
        ...
