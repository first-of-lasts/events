from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from events.domain.exceptions.database import DatabaseIntegrityError
from events.application.interfaces import auth_interface
from events.infrastructure.adapters.database.user import User
from events.infrastructure.adapters.auth.token import JwtTokenProcessor, TokenType
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

    # async def save(self, user: UserDM) -> None:
    #     try:
    #         new_user = User(
    #             email=user.email,
    #             username=user.username,
    #             password=user.password,
    #         )
    #         self._session.add(new_user)
    #         await self._session.commit()
    #     except IntegrityError as e:
    #         raise DatabaseIntegrityError(str(e))


    async def save(self, user: UserDM) -> dict:
        async with self._session.begin():
            query = await self._session.execute(
                select(User)
                .where(
                    (User.email == user.email) |
                    (User.username == user.username)
                )
                .with_for_update()
            )
            existing_user = query.scalar()
            if existing_user:
                if existing_user.email == user.email:
                    return {"success": False, "reason": "email_exists"}
                if existing_user.username == user.username:
                    return {"success": False, "reason": "username_exists"}
            new_user = User(
                email=user.email,
                username=user.username,
                password=user.password,
            )
            self._session.add(new_user)
            return {'success': True, "reason": ""}

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
            select(User).where(User.email == email)
        )
        user = result.scalars().one_or_none()
        if user:
            return UserDM(
                username=user.username,
                email=user.email,
                password=user.password,
                is_verified=user.is_verified,
            )

    def create_access_token(self, user_email: str) -> str:
        return self._token_processor.create_access_token(user_email)

    def create_password_reset_token(self, user_email: str) -> str:
        return self._token_processor.create_password_reset_token(user_email)

    def create_refresh_token(self, user_email: str) -> str:
        return self._token_processor.create_refresh_token(user_email)

    def verify_token(self, token: str, token_type: Optional[TokenType] = None) -> str:
        return self._token_processor.verify_token(token, token_type)
