from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from events.domain.exceptions.user import UserNotFoundError
from events.domain.models.user import UserDM
from events.application.interfaces import user_interface
from events.infrastructure.adapters.database.user import User


class UserGateway(
    user_interface.UserUpdater,
    user_interface.UserReader,
):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def update(self, email: str, update_data: dict) -> UserDM:
        result = await self._session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalars().one_or_none()
        if not user:
            raise  UserNotFoundError
        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)
        await self._session.commit()
        return UserDM(
            username=user.username,
            email=user.email,
            bio=user.bio,
        )

    async def get_by_email(self, email: str) -> UserDM:
        result = await self._session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalars().one_or_none()
        if user:
            return UserDM(
                username=user.username,
                email=user.email,
                bio=user.bio,
            )
        else:
            raise UserNotFoundError
