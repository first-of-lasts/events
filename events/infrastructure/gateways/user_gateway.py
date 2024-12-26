from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from events.domain.models.region import RegionDM
from events.domain.models.country import CountryDM
from events.domain.models.user import UserDM
from events.domain.exceptions.user import UserNotFoundError
from events.domain.exceptions.region import InvalidRegionError
from events.application.interfaces import user_interface
from events.infrastructure.persistence.models.user import User
from events.infrastructure.persistence.models import Region


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
            .options(selectinload(User.country), selectinload(User.region))
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
            return UserDM(
                id=user.id,
                username=user.username,
                email=user.email,
                bio=user.bio,
                country=country_dm,
                region=region_dm,
            )
        else:
            raise UserNotFoundError

    async def update(self, email: str, update_data: dict) -> None:
        result = await self._session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalars().one_or_none()
        if not user:
            raise UserNotFoundError
        #
        new_country_id = update_data.get('country_id', user.country_id)
        new_region_id = update_data.get('region_id', user.region_id)
        if new_region_id:
            if not new_country_id:
                raise InvalidRegionError
            region_result = await self._session.execute(
                select(Region).where(Region.id == new_region_id)
            )
            region = region_result.scalars().one_or_none()
            if (not region) or (region.country_id != new_country_id):
                raise InvalidRegionError
        #
        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)
        await self._session.commit()
