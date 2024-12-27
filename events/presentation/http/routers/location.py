from fastapi import APIRouter, Depends
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from events.application.interactors import location_interactor
from events.presentation.http.dependencies.language import get_valid_language
from events.presentation.http.dependencies.authentication import get_user_email

location_router = APIRouter()


@location_router.get("/countries")
@inject
async def get_country_list(
        interactor: FromDishka[location_interactor.GetCountriesInteractor],
        user_email: str = Depends(get_user_email),
        language: str = Depends(get_valid_language),
):
    return await interactor(language=language)


@location_router.get("/countries/{country_id}/regions")
@inject
async def get_regions_list(
        country_id: int,
        interactor: FromDishka[location_interactor.GetRegionsInteractor],
        user_email: str = Depends(get_user_email),
        language: str = Depends(get_valid_language),
):
    return await interactor(country_id=country_id, language=language)
