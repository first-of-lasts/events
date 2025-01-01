from fastapi import APIRouter, Depends
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from events.application.interactors import user_interactor
from events.application.schemas.requests import user_request
from events.application.schemas.responses import user_response
from events.presentation.http.dependencies.authentication import get_user_id
from events.presentation.http.dependencies.language import get_valid_language


user_router = APIRouter()


@user_router.get("/me")
@inject
async def get_current_user(
        interactor: FromDishka[user_interactor.GetCurrentUserInteractor],
        user_id: int = Depends(get_user_id),
        language: str = Depends(get_valid_language),
) -> user_response.CurrentUser:
    user = await interactor(user_id=user_id, language=language)
    return user


@user_router.put("/me")
@inject
async def update_current_user(
        data: user_request.CurrentUserUpdate,
        interactor: FromDishka[user_interactor.UpdateCurrentUserInteractor],
        user_id: int = Depends(get_user_id),
):
    await interactor(dto=data, user_id=user_id)
    return {"message": "User updated successfully"}
