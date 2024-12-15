from abc import abstractmethod
from typing import Protocol, Optional

from events.domain.models.user import UserDM


class UserUpdater(Protocol):
    @abstractmethod
    async def update(self, email: str, update_data: dict) -> UserDM:
        """
        Updates existing user
        """
        ...


class UserReader(Protocol):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserDM]:
        """
        Retrieves a user by email.
        Returns None if the user does not exist.
        """
        ...
