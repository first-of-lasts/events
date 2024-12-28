from fastapi import APIRouter, Depends
from dishka.integrations.base import FromDishka
from dishka.integrations.fastapi import inject

from events.application.dto.auth import NewUserDTO
from events.application.interactors import auth_interactor
from events.presentation.http.dependencies.language import get_valid_language
from events.presentation.http.schemas import auth as schemas


auth_router = APIRouter()


@auth_router.post("/register")
@inject
async def register(
        data: schemas.Register,
        interactor: FromDishka[auth_interactor.RegisterInteractor],
        language: str = Depends(get_valid_language),
):
    dto = NewUserDTO(
        email=str(data.email),
        username=data.username,
        password=data.password,
    )
    await interactor(user_dto=dto, language=language)
    return {"message": "User created successfully"}


@auth_router.get("/verify-email")
@inject
async def verify(
        token: str,
        interactor: FromDishka[auth_interactor.VerifyInteractor],
):
    await interactor(token)
    return {"message": "User verified successfully"}


@auth_router.post("/login")
@inject
async def login(
        data: schemas.Login,
        interactor: FromDishka[auth_interactor.LoginInteractor],
):
    tokens = await interactor(email=str(data.email), password=data.password)
    return tokens


@auth_router.post("/password-reset")
@inject
async def password_reset(
        data: schemas.PasswordReset,
        interactor: FromDishka[auth_interactor.PasswordResetInteractor],
        language: str = Depends(get_valid_language),
):
    await interactor(email=str(data.email), language=language)
    return {"message": "Reset link was successfully sent"}


@auth_router.post("/password-reset/confirm")
@inject
async def password_reset_confirm(
        data: schemas.PasswordResetConfirm,
        interactor: FromDishka[auth_interactor.PasswordResetConfirmInteractor]
):
    await interactor(data.token, data.new_password)
    return {"message": "New password has been successfully set"}


@auth_router.post("/create-token-pair")
@inject
async def create_token_pair(
        data: schemas.CreateTokenPair,
        interactor: FromDishka[auth_interactor.CreateTokenPairInteractor]
):
    return await interactor(refresh=data.refresh_token)
