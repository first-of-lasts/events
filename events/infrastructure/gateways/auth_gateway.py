from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from events.application.interfaces import auth_interface
from events.domain.exceptions.user import UserCannotBeCreatedError
from events.infrastructure.adapters.database.user import User
from events.domain.models.user import UserDM


class AuthGateway(
    auth_interface.UserSaver,
    auth_interface.UserUpdater,
    auth_interface.UserReader,
):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, user: UserDM) -> None:
        try:
            new_user = User(
                email=user.email,
                username=user.username,
                password=user.password,
            )
            self._session.add(new_user)
            await self._session.commit()
        except IntegrityError as e:
            if "email" in str(e.orig):
                raise UserCannotBeCreatedError("Email already exists")
            elif "username" in str(e.orig):
                raise UserCannotBeCreatedError("Username already exists")
            else:
                raise UserCannotBeCreatedError("User creation failed")

    async def update(self, email: str, update_data: dict) -> None:
        stmt = (
            update(User)
            .where(User.email == email)
            .values(**update_data)
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self._session.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().one_or_none()
