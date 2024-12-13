from fastapi import APIRouter, Depends, HTTPException
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from events.domain.exceptions.user import UserNotFoundError
from events.application.interactors import user_interactor
from events.main.authentication import get_user_email
from events.presentation.http.user.schemas import request as request_schemas
from events.presentation.http.user.schemas import response as response_schemas


user_router = APIRouter()


@user_router.get("/me")
@inject
async def get_user(
        interactor: FromDishka[user_interactor.GetUserInteractor],
        user_email: str = Depends(get_user_email),
) -> response_schemas.UserResponse:
    try:
        user = await interactor(user_email)
        return response_schemas.UserResponse(
           email=user.email,
           username=user.username,
           bio=user.bio,
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )


@user_router.patch("/me")
@inject
async def update_user(
        updates: request_schemas.UpdateUserRequest,
        interactor: FromDishka[user_interactor.UpdateUserInteractor],
        user_email: str = Depends(get_user_email),
) -> response_schemas.UserResponse:
    try:
        user = await interactor(user_email, dict(updates))
        return response_schemas.UserResponse(
            email=user.email,
            username=user.username,
            bio=user.bio,
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
