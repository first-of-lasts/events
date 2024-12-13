from fastapi import APIRouter, status, HTTPException
from dishka.integrations.base import FromDishka
from dishka.integrations.fastapi import inject

from events.domain.exceptions.access import AuthenticationError
from events.domain.exceptions.user import UserCannotBeCreatedError
from events.application.interactors import auth_interactor
from events.application.dto import auth_dto
from events.presentation.http.auth.schemas import request as request_schemas
from events.presentation.http.auth.schemas import response as response_schemas


auth_router = APIRouter()


@auth_router.post("/register")
@inject
async def register(
        data: request_schemas.RegisterRequest,
        interactor: FromDishka[auth_interactor.RegisterInteractor]
):
    try:
        dto = auth_dto.NewUserDTO(
            email=str(data.email),
            username=data.username,
            password=data.password,
        )
        await interactor(dto)
        return {"message": "User created successfully"}
    except UserCannotBeCreatedError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.reason,
        )


@auth_router.get("/verify-email")
@inject
async def verify(
        token: str,
        interactor: FromDishka[auth_interactor.VerifyInteractor]
):
    try:
        await interactor(token)
        return {"message": "User verified successfully"}
    except AuthenticationError:
        raise HTTPException(
            status_code=401, detail="Authentication failed"
        )


@auth_router.post("/login")
@inject
async def login(
        data: request_schemas.LoginRequest,
        interactor: FromDishka[auth_interactor.LoginInteractor]
):
    try:
        dto = auth_dto.LoginUserDTO(
            email=str(data.email),
            password=data.password
        )
        tokens = await interactor(dto)
        return tokens
    except AuthenticationError:
        raise HTTPException(
            status_code=401, detail="Authentication failed"
        )


@auth_router.post("/password-reset")
@inject
async def password_reset(
        data: request_schemas.PasswordResetRequest,
        interactor: FromDishka[auth_interactor.PasswordResetInteractor]
):
    await interactor(str(data.email))
    return {"message": "Reset link was successfully sent"}


@auth_router.post("/password-reset-confirm")
@inject
async def password_reset_confirm(
        data: request_schemas.PasswordResetConfirmRequest,
        interactor: FromDishka[auth_interactor.PasswordResetConfirmInteractor]
):
    try:
        await interactor(data.token, data.new_password)
        return {"message": "New password has been successfully set"}
    except AuthenticationError:
        raise HTTPException(
            status_code=401, detail="Authentication failed"
        )
