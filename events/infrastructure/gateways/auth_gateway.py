from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from events.application.interfaces import auth_interface
from events.infrastructure.persistence.models.user import User
from events.infrastructure.auth.token import JwtTokenProcessor, TokenType
from events.domain.models.user import UserDM


class AuthGateway(
    auth_interface.UserSaver,
    auth_interface.UserUpdater,
    auth_interface.UserReader,
    auth_interface.TokenProcessor,
):
    def __init__(self, session: AsyncSession, token_processor: JwtTokenProcessor):
        self._session = session
        self._token_processor = token_processor

    async def delete_inactive_by_email(self, email: str) -> None:
        stmt = select(User).where(User.email == email).with_for_update()
        result = await self._session.execute(stmt)
        user = result.scalars().one_or_none()
        if user and not user.is_verified:
            await self._session.delete(user)
            await self._session.flush()

    async def exists_by_email(self, email: str) -> bool:
        stmt = select(User).where(User.email == email).limit(1)
        result = await self._session.execute(stmt)
        return result.scalars().one_or_none() is not None

    async def exists_by_username(self, username: str) -> bool:
        stmt = select(User).where(User.username == username).limit(1)
        result = await self._session.execute(stmt)
        return result.scalars().one_or_none() is not None

    async def save(self, user: UserDM):
        new_user = User(
            email=user.email,
            username=user.username,
            password=user.password,
        )
        self._session.add(new_user)

    async def update(self, email: str, update_data: dict) -> None:
        stmt = (
            update(User)
            .where(User.email == email)
            .values(**update_data)
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_by_email(self, email: str) -> Optional[UserDM]:
        result = await self._session.execute(
            select(User)
            .where(User.email == email, User.is_verified == True, User.is_active == True)
        )
        user = result.scalars().one_or_none()
        if user:
            return UserDM(
                id=user.id,
                username=user.username,
                email=user.email,
                password=user.password,
                is_verified=user.is_verified,
                is_active=user.is_active,
            )

    def create_access_token(self, user_email: str) -> str:
        return self._token_processor.create_access_token(user_email)

    def create_password_reset_token(self, user_email: str) -> str:
        return self._token_processor.create_password_reset_token(user_email)

    def create_refresh_token(self, user_email: str) -> str:
        return self._token_processor.create_refresh_token(user_email)

    def verify_token(self, token: str, token_type: Optional[TokenType] = None) -> str:
        return self._token_processor.verify_token(token, token_type)
