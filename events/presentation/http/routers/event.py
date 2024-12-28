from fastapi import APIRouter, Depends
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from events.application.interactors import event_interactor
from events.application.dto.event import NewEventDTO
from events.presentation.http.dependencies.authentication import get_user_email
from events.presentation.http.schemas import event as schemas


event_router = APIRouter()


@event_router.post("/",)
@inject
async def create_event(
        data: schemas.CreateEvent,
        interactor: FromDishka[event_interactor.CreateEventInteractor],
        user_email: str = Depends(get_user_email),
):
    dto = NewEventDTO(
        title=data.title,
        description=data.description,
        country_id=data.country_id,
        region_id=data.region_id
    )
    await interactor(event_dto=dto, email=user_email)
    return {"message": "Event created successfully"}
