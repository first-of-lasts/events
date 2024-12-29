from abc import abstractmethod
from typing import Protocol, Optional

from events.domain.models.user import UserDM
from events.infrastructure.auth.token import TokenType


class UserCreator(Protocol):
    @abstractmethod
    async def delete_inactive_by_email(self, email: str) -> None:
        ...

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        ...

    @abstractmethod
    async def exists_by_username(self, email: str) -> bool:
        ...

    @abstractmethod
    async def create_user(self, user: UserDM):
        ...


class UserUpdater(Protocol):
    @abstractmethod
    async def update(self, email: str, update_data: dict) -> None:
        ...


class TokenProcessor(Protocol):
    @abstractmethod
    def create_access_token(self, user_email: str) -> str:
        ...

    @abstractmethod
    def create_password_reset_token(self, user_email: str) -> str:
        ...

    @abstractmethod
    def create_refresh_token(self, user_email: str) -> str:
        ...

    @abstractmethod
    def verify_token(self, token: str, token_type: Optional[TokenType] = None) -> str:
        ...
