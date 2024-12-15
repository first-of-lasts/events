from abc import abstractmethod
from typing import Protocol, Optional

from events.domain.models.user import UserDM
from events.infrastructure.adapters.auth.token import TokenType


class UserSaver(Protocol):
    @abstractmethod
    async def save(self, user: UserDM) -> dict:
        """
        Saves new user.
        """
        ...


class UserUpdater(Protocol):
    @abstractmethod
    async def update(self, email: str, update_data: dict) -> None:
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


class TokenProcessor(Protocol):
    @abstractmethod
    def create_access_token(self, user_email: str) -> str:
        """
        Creates access token
        """
        ...

    @abstractmethod
    def create_password_reset_token(self, user_email: str) -> str:
        """
        Creates password reset token
        """
        ...

    @abstractmethod
    def create_refresh_token(self, user_email: str) -> str:
        """
        Creates refresh token
        """
        ...

    @abstractmethod
    def verify_token(self, token: str, token_type: Optional[TokenType] = None) -> str:
        """
        Verifies token
        """
        ...
