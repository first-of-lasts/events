from fastapi import APIRouter, Depends, HTTPException
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from events.domain.exceptions.user import UserNotFoundError
from events.domain.exceptions.region import InvalidRegionError
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
    try:
        user = await interactor(email=user_email, language=language)
        return user
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@user_router.patch("/me")
@inject
async def update_user(
        updates: schemas.UpdateUser,
        interactor: FromDishka[user_interactor.UpdateUserInteractor],
        user_email: str = Depends(get_user_email),
):
    try:
        await interactor(user_email, dict(updates))
        return {"message": "User updated successfully"}
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except InvalidRegionError:
        raise HTTPException(status_code=400, detail="Invalid region")
