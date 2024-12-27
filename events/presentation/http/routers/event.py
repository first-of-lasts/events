from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

from events.application.interactors import event_interactor
from events.presentation.http.dependencies.authentication import get_user_email


event_router = APIRouter()


@event_router.post("/")
@inject
async def create_event(
        interactor: FromDishka[event_interactor.CreateEventInteractor],
        user_email: str = Depends(get_user_email),
):
    await interactor(user_email)
    return {"message": "Event created successfully"}
