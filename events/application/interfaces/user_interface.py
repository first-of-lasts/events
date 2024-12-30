from abc import abstractmethod
from typing import Protocol, Optional

from events.domain.models.user import UserDM


class UserUpdater(Protocol):
    @abstractmethod
    async def update(self, email: str, update_data: dict) -> None:
        ...


class UserReader(Protocol):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserDM]:
        ...

    @abstractmethod
    async def get_by_email_with_details(self, email: str, language: str) -> Optional[UserDM]:
        ...
