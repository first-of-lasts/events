from fastapi import APIRouter, Depends
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from events.application.interactors import user_interactor
from events.presentation.http.dependencies.authentication import get_user_email
from events.presentation.http.dependencies.language import get_valid_language
from events.presentation.http.schemas import user as schemas


user_router = APIRouter()


@user_router.get("/me")
@inject
async def get_user(
        interactor: FromDishka[user_interactor.GetUserInteractor],
        user_email: str = Depends(get_user_email),
        language: str = Depends(get_valid_language),
): # TODO -> schemas.GetUser:
    user = await interactor(email=user_email, language=language)
    return user


@user_router.patch("/me")
@inject
async def update_user(
        updates: schemas.UpdateUser,
        interactor: FromDishka[user_interactor.UpdateUserInteractor],
        user_email: str = Depends(get_user_email),
):
    await interactor(user_email, dict(updates))
    return {"message": "User updated successfully"}
