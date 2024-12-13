from abc import abstractmethod
from typing import Protocol, Optional

from events.domain.models.user import UserDM


class UserReader(Protocol):
    @abstractmethod
    async def get_by_email(self, email: str):
        """
        Retrieves a user by email.
        Returns None if the user does not exist.
        """
        ...


class UserUpdater(Protocol):
    @abstractmethod
    async def update(self, email: str, update_data: dict):
        """
        Updates existing user
        """
        ...
