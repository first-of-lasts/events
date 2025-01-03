from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from events.domain.models.region import RegionDM
from events.domain.models.country import CountryDM
from events.domain.models.user import UserDM
from events.application.interfaces import user_interface
from events.application.schemas.responses import user_response
from events.infrastructure.persistence.models import User


class UserGateway(
    user_interface.UserUpdater,
    user_interface.UserReader,
):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user(self, email: str) -> Optional[UserDM]:
        result = await self._session.execute(
            select(User)
            .where(User.email == email, User.is_verified == True, User.is_blacklisted == False)
            .limit(1)
        )
        user = result.scalars().one_or_none()
        if user:
            return UserDM(
                id=user.id,
                email=user.email,
                username=user.username,
            )

    async def get_login_user(self, email: str) -> Optional[UserDM]:
        result = await self._session.execute(
            select(User)
            .where(User.email == email, User.is_verified == True, User.is_blacklisted == False)
            .limit(1)
        )
        user = result.scalars().one_or_none()
        if user:
            return UserDM(
                id=user.id,
                password=user.password,
                is_verified=user.is_verified,
                is_blacklisted=user.is_blacklisted,
            )

    async def get_detailed_user(
            self,
            user_id: int,
            language: str
    ) -> Optional[user_response.CurrentUser]:
        result = await self._session.execute(
            select(User)
            .where(User.id == user_id, User.is_verified == True, User.is_blacklisted == False)
            .options(selectinload(User.country), selectinload(User.region))
            .limit(1)
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
            region_dm = None
            if user.region:
                region_dm = RegionDM(
                    id=user.region.id,
                    name=user.region.get_name(language),
                )
            return user_response.CurrentUser(
                id=user.id,
                email=user.email,
                username=user.username,
                bio=user.bio,
                country=country_dm,
                region=region_dm,
            )

    async def update_user(self, user_id: int, update_data: dict) -> None:
        await self._session.execute(
            update(User)
            .where(User.id == user_id)
            .values(**update_data)
        )
        await self._session.commit()
