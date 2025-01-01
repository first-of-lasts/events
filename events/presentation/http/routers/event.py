from fastapi import APIRouter, Depends
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from events.application.interactors import event_interactor
from events.application.dto import event as event_dto
from events.presentation.http.dependencies.authentication import get_user_email
from events.presentation.http.dependencies.language import get_valid_language


event_router = APIRouter()


@event_router.get("")
@inject
async def list_user_events(
        interactor: FromDishka[event_interactor.ListUserEventsInteractor],
        dto: event_dto.ListUserEventsDTO = Depends(),
        user_email: str = Depends(get_user_email),
        language: str = Depends(get_valid_language),
):
    events = await interactor(dto=dto, user_email=user_email, language=language)
    return events


@event_router.post("")
@inject
async def create_event(
        data: event_dto.NewEventDTO,
        interactor: FromDishka[event_interactor.CreateEventInteractor],
        user_email: str = Depends(get_user_email),
):
    await interactor(dto=data, user_email=user_email)
    return {"message": "Event created successfully"}


@event_router.put("/{event_id}")
@inject
async def update_event(
        event_id: int,
        data: event_dto.UpdateEventDTO,
        interactor: FromDishka[event_interactor.UpdateEventInteractor],
        user_email: str = Depends(get_user_email),
):
    await interactor(dto=data, user_email=user_email, event_id=event_id)
    return {"message": "Event updated successfully"}



# @event_router.delete("")
# @inject
# async def delete_event(
#
# ):
#     pass
