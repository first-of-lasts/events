from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from events.domain.models.country import CountryDM
from events.domain.models.region import RegionDM
from events.domain.exceptions.country import CountryNotFoundError
from events.application.interfaces import location_interface
from events.infrastructure.persistence.models import Country
from events.infrastructure.persistence.models import Region


class LocationGateway(
    location_interface.CountryReader,
    location_interface.RegionReader,
):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def exists_country_by_id(self, country_id: int) -> bool:
        result =  await self._session.execute(
            select(Country)
            .where(Country.id == country_id)
            .limit(1)
        )
        return result.scalars().one_or_none() is not None

    async def get_country_list(self, language: str) -> List[CountryDM]:
        result = await self._session.execute(select(Country))
        countries = result.scalars().all()
        country_list = []
        for country in countries:
            country_list.append(
                CountryDM(
                    id=country.id,
                    code=country.code,
                    name= country.get_name(language)
                )
            )
        return country_list

    async def get_region(self, region_id: int) -> Optional[RegionDM]:
        result = await self._session.execute(
            select(Region)
            .where(Region.id == region_id)
            .limit(1)
        )
        region = result.scalars().one_or_none()
        if region:
            return RegionDM(
                id=region.id,
                country_id=region.country_id,
            )

    async def get_region_list(self, country_id: int, language: str) -> List[RegionDM]:
        country_exists = await self._session.execute(
            select(Country.id).where(Country.id == country_id)
        )
        if not country_exists.scalars().first():
            raise CountryNotFoundError("Country does not exist")
        result = await self._session.execute(
            select(Region).where(Region.country_id == country_id)
        )
        regions = result.scalars().all()
        region_list = []
        for region in regions:
            region_dm = RegionDM(
                id=region.id,
                name=region.get_name(language)
            )
            region_list.append(region_dm)
        return region_list
