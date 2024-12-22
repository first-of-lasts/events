from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from events.domain.models.country import CountryDM
from events.domain.exceptions.user import UserNotFoundError
from events.domain.models.user import UserDM
from events.application.interfaces import user_interface
from events.infrastructure.persistence.models.user import User


class UserGateway(
    user_interface.UserUpdater,
    user_interface.UserReader,
):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_email(self, email: str, language: str) -> UserDM:
        result = await self._session.execute(
            select(User)
            .where(User.email == email, User.is_verified == True, User.is_active == True)
            .options(selectinload(User.country),) # selectinload(User.region))
        )
        user = result.scalars().one_or_none()
        if user:
            country_dm = None
            if user.country:
                country_dm = CountryDM(
                    id=user.country.id,
                    code=user.country.code,
                    name=user.country.get_name(language)
                )
            # region_dm = None
            # if user.region:
            #     region_dm = RegionDM(
            #
            #     )
            return UserDM(
                id=user.id,
                username=user.username,
                email=user.email,
                bio=user.bio,
                country=country_dm
            )
        else:
            raise UserNotFoundError

    async def update(self, email: str, update_data: dict) -> None:
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
