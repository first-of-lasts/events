from events.application.utils.security import verify_password, hash_password
from events.domain.exceptions.access import AuthenticationError
from events.infrastructure.adapters.auth.token import JwtTokenProcessor, TokenType
from events.application.interfaces.email_interface import EmailSender
from events.application.dto import auth_dto
from events.application.interfaces import auth_interface
from events.domain.models.user import UserDM


class RegisterInteractor:
    def __init__(
            self,
            auth_gateway: auth_interface.UserSaver,
            email_gateway: EmailSender,
            jwt_token_processor: JwtTokenProcessor,
    ) -> None:
        self._auth_gateway = auth_gateway
        self._email_gateway = email_gateway
        self._jwt_token_processor = jwt_token_processor

    async def __call__(self, dto: auth_dto.NewUserDTO) -> None:
        user = UserDM(
            email=dto.email,
            username=dto.username,
            password=hash_password(dto.password),
        )
        await self._auth_gateway.save(user)
        token = self._jwt_token_processor.create_access_token(dto.email)
        verification_link = f"https://localhost:8000/verify-email?token={token}"
        await self._email_gateway.send_email(
            recipient=dto.email,
            subject="Account verification",
            body=f"Hi {dto.username}, visit the link: {verification_link} to verify account",
        )


class VerifyInteractor:
    def __init__(
            self,
            auth_gateway: auth_interface.UserUpdater,
            jwt_token_processor: JwtTokenProcessor,
    ) -> None:
        self._auth_gateway = auth_gateway
        self._jwt_token_processor = jwt_token_processor

    async def __call__(self, token) -> None:
        email = self._jwt_token_processor.verify_token(
            token, token_type=TokenType.ACCESS
        )
        await self._auth_gateway.update(email, {"is_verified": True})


class LoginInteractor:
    def __init__(
            self,
            auth_gateway: auth_interface.UserReader,
            jwt_token_processor: JwtTokenProcessor,
    ) -> None:
        self._auth_gateway = auth_gateway
        self._jwt_token_processor = jwt_token_processor

    async def __call__(self, dto: auth_dto.LoginUserDTO) -> dict:
        user = await self._auth_gateway.get_by_email(dto.email)
        if not user or not verify_password(dto.password, user.password):
            raise AuthenticationError
        if not user.is_verified:
            raise AuthenticationError

        access_token = self._jwt_token_processor.create_access_token(
            user.email
        )
        refresh_token = self._jwt_token_processor.create_refresh_token(
            user.email
        )
        return {"access_token": access_token, "refresh_token": refresh_token}


class PasswordResetInteractor:
    def __init__(
            self,
            auth_gateway: auth_interface.UserReader,
            email_gateway: EmailSender,
            jwt_token_processor: JwtTokenProcessor,
    ) -> None:
        self._auth_gateway = auth_gateway
        self._email_gateway = email_gateway
        self._jwt_token_processor = jwt_token_processor

    async def __call__(self, email: str) -> None:
        user = await self._auth_gateway.get_by_email(email)
        if user:
            token = self._jwt_token_processor.create_password_reset_token(email)
            reset_link = f"https://localhost:8000/reset-password?token={token}"
            await self._email_gateway.send_email(
                recipient=email,
                subject="Password Reset",
                body=f"Hi, visit the link: {reset_link} to reset your password.",
            )


class PasswordResetConfirmInteractor:
    def __init__(
            self,
            auth_gateway: auth_interface.UserUpdater,
            jwt_token_processor: JwtTokenProcessor,
    ):
        self._auth_gateway = auth_gateway
        self._jwt_token_processor = jwt_token_processor

    async def __call__(self, token: str, password: str) -> None:
        email = self._jwt_token_processor.verify_token(
            token, token_type=TokenType.PASSWORD_RESET
        )
        hashed_password = hash_password(password)
        await self._auth_gateway.update(email, {"password": hashed_password})
