from abc import abstractmethod
from typing import Protocol, Optional

from events.domain.models.user import UserDM
from events.domain.schemas.user import CurrentUser


class UserUpdater(Protocol):
    @abstractmethod
    async def update_user(self, email: str, update_data: dict) -> None:
        ...


class UserReader(Protocol):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserDM]:
        ...

    @abstractmethod
    async def get_by_email_for_login(self, email: str) -> Optional[UserDM]:
        ...

    @abstractmethod
    async def get_current_user(self, email: str, language: str) -> Optional[CurrentUser]:
        ...
