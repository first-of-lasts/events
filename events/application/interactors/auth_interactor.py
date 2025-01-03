import gettext

from events.domain.models.user import UserDM
from events.domain.exceptions.user import UserCannotBeCreatedError
from events.domain.exceptions.access import AuthenticationError
from events.application.interfaces import email_interface, user_interface
from events.application.interfaces import root_interface
from events.application.interfaces import auth_interface
from events.application.schemas.requests import auth_request
from events.application.utils.security import verify_password, hash_password
from events.infrastructure.auth.token import TokenType
from events.main.config import Config


class RegisterInteractor:
    def __init__(
            self,
            config: Config,
            db_session: root_interface.DBSession,
            auth_gateway: auth_interface.UserCreator,
            email_gateway: email_interface.EmailSender,
            token_processor: auth_interface.TokenProcessor,
            translations: dict[str, gettext.GNUTranslations],
    ) -> None:
        self._config = config
        self._db_session = db_session
        self._auth_gateway = auth_gateway
        self._email_gateway = email_gateway
        self._token_processor = token_processor
        self._translations = translations

    async def __call__(self, dto: auth_request.UserCreate, language: str) -> None:
        async with self._db_session.begin():
            await self._auth_gateway.delete_inactive_by_email(str(dto.email))

            email_conflicts = await self._auth_gateway.exists_by_email(str(dto.email))
            if email_conflicts:
                raise UserCannotBeCreatedError("Email already exists")

            username_conflicts = await self._auth_gateway.exists_by_username(dto.username)
            if username_conflicts:
                raise UserCannotBeCreatedError("Username already exists")

            user = UserDM(
                email=str(dto.email),
                username=dto.username,
                password=hash_password(dto.password),
            )
            user_id = await self._auth_gateway.create_user(user)
        await self._send_verification_email(
            user_id=user_id, email=str(dto.email), language=language
        )

    async def _send_verification_email(self, user_id: int, email: str, language: str) -> None:
        _ = self._translations[language].gettext
        #
        token = self._token_processor.create_access_token(user_id)
        verification_link = f"{self._config.app.base_url}/api/v1/auth/verify?token={token}"
        subject = _("Account verification")
        body = _("Visit the link to verify your account: {link}").format(link=verification_link)
        await self._email_gateway.send_email(
            recipient=email, subject=subject, body=body,
        )


class VerifyInteractor:
    def __init__(
            self,
            auth_gateway: auth_interface.UserPrimaryDataUpdater,
            token_processor: auth_interface.TokenProcessor,
    ) -> None:
        self._auth_gateway = auth_gateway
        self._token_processor = token_processor

    async def __call__(self, dto: auth_request.Verify) -> None:
        user_id = self._token_processor.verify_token(
            dto.token, token_type=TokenType.ACCESS
        )
        await self._auth_gateway.verify_user(user_id)


class LoginInteractor:
    def __init__(
            self,
            user_gateway: user_interface.UserReader,
            token_processor: auth_interface.TokenProcessor,
    ) -> None:
        self._user_gateway = user_gateway
        self._token_processor = token_processor

    async def __call__(self, dto: auth_request.Login) -> dict:
        user = await self._user_gateway.get_login_user(str(dto.email))
        if (user and user.is_verified) and (not user.is_blacklisted):
            if not verify_password(dto.password, user.password):
                raise AuthenticationError("Invalid credentials")
        else:
            raise AuthenticationError("Invalid credentials")

        access_token = self._token_processor.create_access_token(user.id)
        refresh_token = self._token_processor.create_refresh_token(user.id)
        return {"access_token": access_token, "refresh_token": refresh_token}


class PasswordResetInteractor:
    def __init__(
            self,
            config: Config,
            user_gateway: user_interface.UserReader,
            email_gateway: email_interface.EmailSender,
            token_processor: auth_interface.TokenProcessor,
            translations: dict[str, gettext.GNUTranslations],
    ) -> None:
        self._config = config
        self._user_gateway = user_gateway
        self._email_gateway = email_gateway
        self._token_processor = token_processor
        self._translations = translations

    async def __call__(self, dto: auth_request.PasswordReset, language: str) -> None:
        user = await self._user_gateway.get_user(str(dto.email))
        if user:
            await self._send_reset_email(user_id=user.id, email=str(dto.email), language=language)

    async def _send_reset_email(self, user_id: int, email: str, language: str) -> None:
        _ = self._translations[language].gettext
        #
        token = self._token_processor.create_password_reset_token(user_id)
        reset_link = f"{self._config.app.base_url}/api/v1/auth/reset-password?token={token}"
        subject = _("Password Reset")
        body = _(
            "Hi, visit the link: {reset_link} to reset your password."
        ).format(reset_link=reset_link)
        await self._email_gateway.send_email(
            recipient=email, subject=subject, body=body,
        )


class PasswordResetConfirmInteractor:
    def __init__(
            self,
            auth_gateway: auth_interface.UserPrimaryDataUpdater,
            token_processor: auth_interface.TokenProcessor,
    ) -> None:
        self._auth_gateway = auth_gateway
        self._token_processor = token_processor

    async def __call__(self, dto: auth_request.PasswordResetConfirm) -> None:
        user_id = self._token_processor.verify_token(
            dto.token, token_type=TokenType.PASSWORD_RESET
        )
        new_password = hash_password(dto.new_password)
        await self._auth_gateway.change_user_password(user_id, new_password)


class CreateTokenPairInteractor:
    def __init__(
            self,
            token_processor: auth_interface.TokenProcessor,
    ) -> None:
        self._token_processor = token_processor

    async def __call__(self, dto: auth_request.CreateTokenPair) -> dict:
        user_id = self._token_processor.verify_token(
            dto.refresh_token, token_type=TokenType.REFRESH
        )
        access_token = self._token_processor.create_access_token(user_id)
        refresh_token = self._token_processor.create_refresh_token(user_id)
        return {"access_token": access_token, "refresh_token": refresh_token}
