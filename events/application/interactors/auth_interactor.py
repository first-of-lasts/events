import gettext

from events.domain.models.user import UserDM
from events.domain.exceptions.user import UserCannotBeCreatedError
from events.domain.exceptions.access import AuthenticationError
from events.application.interfaces import email_interface, user_interface
from events.application.interfaces import root_interface
from events.application.interfaces import auth_interface
from events.application.dto import auth as auth_dto
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

    async def __call__(self, dto: auth_dto.NewUserDTO, language: str) -> None:
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
            await self._auth_gateway.create_user(user)
        await self._send_verification_email(email=str(dto.email), language=language)

    async def _send_verification_email(self, email: str, language: str) -> None:
        _ = self._translations[language].gettext
        #
        token = self._token_processor.create_access_token(email)
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

    async def __call__(self, token: str) -> None:
        email = self._token_processor.verify_token(
            token, token_type=TokenType.ACCESS
        )
        await self._auth_gateway.verify_user(email)


class LoginInteractor:
    def __init__(
            self,
            user_gateway: user_interface.UserReader,
            token_processor: auth_interface.TokenProcessor,
    ) -> None:
        self._user_gateway = user_gateway
        self._token_processor = token_processor

    async def __call__(self, email: str, password: str) -> dict:
        user = await self._user_gateway.get_by_email(email)
        if user and user.is_verified and user.is_active:
            if not verify_password(password, user.password):
                raise AuthenticationError("Invalid credentials")
        else:
            raise AuthenticationError("Invalid credentials")

        access_token = self._token_processor.create_access_token(
            user.email
        )
        refresh_token = self._token_processor.create_refresh_token(
            user.email
        )
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

    async def __call__(self, email: str, language: str) -> None:
        user = await self._user_gateway.get_by_email(email)
        if user:
            await self._send_reset_email(email=email, language=language)

    async def _send_reset_email(self, email: str, language: str) -> None:
        _ = self._translations[language].gettext
        #
        token = self._token_processor.create_password_reset_token(email)
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

    async def __call__(self, token: str, new_password: str) -> None:
        email = self._token_processor.verify_token(
            token, token_type=TokenType.PASSWORD_RESET
        )
        new_password = hash_password(new_password)
        await self._auth_gateway.change_user_password(email, new_password)


class CreateTokenPairInteractor:
    def __init__(
            self,
            token_processor: auth_interface.TokenProcessor,
    ) -> None:
        self._token_processor = token_processor

    async def __call__(self, refresh: str) -> dict:
        email = self._token_processor.verify_token(
            refresh, token_type=TokenType.REFRESH
        )
        access_token = self._token_processor.create_access_token(email)
        refresh_token = self._token_processor.create_refresh_token(email)
        return {"access_token": access_token, "refresh_token": refresh_token}
