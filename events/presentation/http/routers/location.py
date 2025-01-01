from typing import List

from fastapi import APIRouter, Depends
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from events.application.interactors import location_interactor
from events.application.schemas.responses import location_response
from events.presentation.http.dependencies.language import get_valid_language
from events.presentation.http.dependencies.authentication import get_user_id


location_router = APIRouter()


@location_router.get("/countries")
@inject
async def list_countries(
        interactor: FromDishka[location_interactor.ListCountriesInteractor],
        user_id: int = Depends(get_user_id),
        language: str = Depends(get_valid_language),
) -> List[location_response.CountryList]:
    return await interactor(language=language)


@location_router.get("/countries/{country_id}/regions")
@inject
async def list_regions(
        country_id: int,
        interactor: FromDishka[location_interactor.ListRegionsInteractor],
        user_id: int = Depends(get_user_id),
        language: str = Depends(get_valid_language),
) -> List[location_response.RegionList]:
    return await interactor(country_id=country_id, language=language)
