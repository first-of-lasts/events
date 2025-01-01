from fastapi import APIRouter, Depends
from dishka.integrations.base import FromDishka
from dishka.integrations.fastapi import inject

from events.application.interactors import auth_interactor
from events.application.schemas.requests import auth_request
from events.presentation.http.dependencies.language import get_valid_language


auth_router = APIRouter()


@auth_router.post("/register")
@inject
async def register(
        data: auth_request.UserCreate,
        interactor: FromDishka[auth_interactor.RegisterInteractor],
        language: str = Depends(get_valid_language),
):
    await interactor(dto=data, language=language)
    return {"message": "User created successfully"}


@auth_router.get("/verify")
@inject
async def verify(
        interactor: FromDishka[auth_interactor.VerifyInteractor],
        data: auth_request.Verify = Depends(),
):
    await interactor(dto=data)
    return {"message": "User verified successfully"}


@auth_router.post("/login")
@inject
async def login(
        data: auth_request.Login,
        interactor: FromDishka[auth_interactor.LoginInteractor],
):
    tokens = await interactor(dto=data)
    return tokens


@auth_router.post("/password-reset")
@inject
async def password_reset(
        data: auth_request.PasswordReset,
        interactor: FromDishka[auth_interactor.PasswordResetInteractor],
        language: str = Depends(get_valid_language),
):
    await interactor(dto=data, language=language)
    return {"message": "Reset link was successfully sent"}


@auth_router.post("/password-reset/confirm")
@inject
async def password_reset_confirm(
        data: auth_request.PasswordResetConfirm,
        interactor: FromDishka[auth_interactor.PasswordResetConfirmInteractor]
):
    await interactor(dto=data)
    return {"message": "New password has been successfully set"}


@auth_router.post("/create-token-pair")
@inject
async def create_token_pair(
        data: auth_request.CreateTokenPair,
        interactor: FromDishka[auth_interactor.CreateTokenPairInteractor]
):
    return await interactor(dto=data)
