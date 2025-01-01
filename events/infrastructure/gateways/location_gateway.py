from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from events.domain.exceptions.location import CountryNotFoundError
from events.application.interfaces.location_interface import LocationGatewayInterface
from events.application.schemas.responses import location_response
from events.infrastructure.persistence.models import Country
from events.infrastructure.persistence.models import Region


class LocationGateway(
    LocationGatewayInterface,
):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def exists_country_by_id(self, country_id: int,) -> bool:
        result =  await self._session.execute(
            select(Country)
            .where(Country.id == country_id)
            .limit(1)
        )
        return result.scalars().one_or_none() is not None

    async def get_countries_list(
            self,
            language: str,
    ) -> List[location_response.CountryList]:
        result = await self._session.execute(select(Country))
        countries = result.scalars().all()
        country_list = [
            location_response.CountryList(
                id=country.id,
                code=country.code,
                name=country.get_name(language)
            )
            for country in countries
        ]
        return country_list

    async def get_region_country_id(self, region_id: int) -> Optional[int]:
        result = await self._session.execute(
            select(Region)
            .where(Region.id == region_id)
            .limit(1)
        )
        region = result.scalars().one_or_none()
        if region:
            return region.country_id

    async def get_regions_list(
            self,
            country_id: int,
            language: str,
    ) -> List[location_response.RegionList]:
        country_exists = await self._session.execute(
            select(Country.id)
            .where(Country.id == country_id)
        )
        if not country_exists.scalars().first():
            raise CountryNotFoundError("Country does not exist")
        result = await self._session.execute(
            select(Region)
            .where(Region.country_id == country_id)
        )
        regions = result.scalars().all()
        region_list = [
            location_response.RegionList(
                id=region.id,
                name=region.get_name(language)
            )
            for region in regions
        ]
        return region_list
