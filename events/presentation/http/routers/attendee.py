from typing import List

from fastapi import APIRouter, Depends
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from events.application.interactors import attendee_interactor
from events.application.schemas.requests import attendee_request
from events.application.schemas.responses import attendee_response
from events.presentation.http.dependencies.authentication import get_user_id
from events.presentation.http.dependencies.language import get_valid_language


attendee_router = APIRouter()


@attendee_router.post("")
@inject
async def create_attendee(
        data: attendee_request.AttendeeCreate,
        interactor: FromDishka[attendee_interactor.CreateAttendeeInteractor],
        user_id: int = Depends(get_user_id),
):
    await interactor(dto=data, user_id=user_id)
    return {"message": "Attendee created successfully"}
