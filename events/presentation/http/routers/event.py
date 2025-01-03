from typing import List

from fastapi import APIRouter, Depends
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from events.application.interactors import event_interactor
from events.application.schemas.requests import event_request
from events.application.schemas.responses import event_response
from events.presentation.http.dependencies.authentication import get_user_id
from events.presentation.http.dependencies.language import get_valid_language


event_router = APIRouter()


@event_router.post("")
@inject
async def create_event(
        data: event_request.EventCreate,
        interactor: FromDishka[event_interactor.CreateEventInteractor],
        user_id: int = Depends(get_user_id),
):
    await interactor(dto=data, user_id=user_id)
    return {"message": "Event created successfully"}


@event_router.put("/{event_id}")
@inject
async def update_event(
        event_id: int,
        data: event_request.EventUpdate,
        interactor: FromDishka[event_interactor.UpdateEventInteractor],
        user_id: int = Depends(get_user_id),
):
    await interactor(dto=data, user_id=user_id, event_id=event_id)
    return {"message": "Event updated successfully"}


@event_router.get("")
@inject
async def list_user_events(
        interactor: FromDishka[event_interactor.ListUserEventsInteractor],
        dto: event_request.UserEventListFilter = Depends(),
        user_id: int = Depends(get_user_id),
        language: str = Depends(get_valid_language),
) -> List[event_response.UserEventList]:
    events = await interactor(dto=dto, user_id=user_id, language=language)
    return events


@event_router.delete("/{event_id}")
@inject
async def delete_event(
        event_id: int,
        interactor: FromDishka[event_interactor.DeleteEventInteractor],
        user_id: int = Depends(get_user_id),
):
    await interactor(user_id=user_id, event_id=event_id)
    return {"message": "Event deleted successfully"}


@event_router.get("/categories")
@inject
async def list_categories(
        interactor: FromDishka[event_interactor.ListCategoriesInteractor],
        user_id: int = Depends(get_user_id),
        language: str = Depends(get_valid_language),
):
    categories = await interactor(language=language)
    return categories
