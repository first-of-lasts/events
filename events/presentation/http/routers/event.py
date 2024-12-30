from fastapi import APIRouter, Depends
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from events.application.interactors import event_interactor
from events.application.dto import event as event_dto
from events.presentation.http.dependencies.authentication import get_user_email
from events.presentation.http.schemas import event as schemas


event_router = APIRouter()


@event_router.post("/",)
@inject
async def create_event(
        data: event_dto.NewEventDTO,
        interactor: FromDishka[event_interactor.CreateEventInteractor],
        user_email: str = Depends(get_user_email),
):
    await interactor(dto=data, email=user_email)
    return {"message": "Event created successfully"}


@event_router.patch("<int:pk>/")
@inject
async def update_event(

):
    pass


@event_router.delete("")
@inject
async def delete_event(

):
    pass
