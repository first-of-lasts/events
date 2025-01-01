from fastapi import APIRouter, Depends
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from events.domain.schemas import user as schemas
from events.application.interactors import user_interactor
from events.application.dto import user as user_dto
from events.presentation.http.dependencies.authentication import get_user_email
from events.presentation.http.dependencies.language import get_valid_language


user_router = APIRouter()


@user_router.get("/me")
@inject
async def get_current_user(
        interactor: FromDishka[user_interactor.GetCurrentUserInteractor],
        user_email: str = Depends(get_user_email),
        language: str = Depends(get_valid_language),
) -> schemas.CurrentUser:
    user = await interactor(user_email=user_email, language=language)
    return user


@user_router.put("/me")
@inject
async def update_current_user(
        data: user_dto.UpdateUserDTO,
        interactor: FromDishka[user_interactor.UpdateCurrentUserInteractor],
        user_email: str = Depends(get_user_email),
):
    await interactor(dto=data, user_email=user_email)
    return {"message": "User updated successfully"}
