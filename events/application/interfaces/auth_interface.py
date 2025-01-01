from abc import abstractmethod
from typing import Protocol

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
    async def create_user(self, user: UserDM) -> int:
        ...


class UserPrimaryDataUpdater(Protocol):
    @abstractmethod
    async def verify_user(self, user_id: int) -> None:
        ...

    @abstractmethod
    async def change_user_password(self, user_id: int, new_password: str) -> None:
        ...


class TokenProcessor(Protocol):
    @abstractmethod
    def create_access_token(self, user_id: int) -> str:
        ...

    @abstractmethod
    def create_password_reset_token(self, user_id: int) -> str:
        ...

    @abstractmethod
    def create_refresh_token(self, user_id: int) -> str:
        ...

    @abstractmethod
    def verify_token(self, token: str, token_type: TokenType) -> int:
        ...
