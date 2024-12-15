import gettext

from sqlalchemy import text

from events.application.utils.security import verify_password, hash_password
from events.domain.exceptions.database import DatabaseIntegrityError
from events.domain.exceptions.user import UserCannotBeCreatedError
from events.domain.exceptions.access import AuthenticationError
from events.infrastructure.adapters.auth.token import TokenType
from events.application.interfaces import email_interface
from events.application.interfaces import root_interface
from events.application.interfaces import auth_interface
from events.application.dto import auth_dto
from events.domain.models.user import UserDM
from events.main.config import Config


class RegisterInteractor:
    def __init__(
            self,
            config: Config,
            db_session: root_interface.DBSession,
            auth_gateway: auth_interface.UserSaver,
            token_processor: auth_interface.TokenProcessor,
            email_gateway: email_interface.EmailSender,
            translations: dict[str, gettext.GNUTranslations],
    ) -> None:
        self._config = config
        self._db_session = db_session
        self._auth_gateway = auth_gateway
        self._email_gateway = email_gateway
        self._token_processor = token_processor
        self._translations = translations

    async def __call__(self, dto: auth_dto.NewUserDTO, language: str) -> None:
        async with self._db_session:
            lock_query = f"LOCK TABLE users IN SHARE ROW EXCLUSIVE MODE"
            await self._db_session.execute(text(lock_query))
            user = UserDM(
                email=dto.email,
                username=dto.username,
                password=hash_password(dto.password),
            )
            if await self._auth_gateway.exists_by_email_or_username(
                    email=dto.email, username=dto.username
            ):
                raise UserCannotBeCreatedError("Email or username already exists")
            await self._auth_gateway.save(user)
        #
        token = self._token_processor.create_access_token(dto.email)
        verification_link = f"{self._config.app.base_url}/verify-email?token={token}"
        # sending email
        if not (language in self._config.app.supported_languages):
            language = "en"
        _ = self._translations[language].gettext
        subject = _("Account verification")
        body = _(
            "Hi {username}, visit the link: {link} to verify your account."
        ).format(username=dto.username,link=verification_link,)
        await self._email_gateway.send_email(
            recipient=dto.email, subject=subject, body=body,
        )


class VerifyInteractor:
    def __init__(
            self,
            auth_gateway: auth_interface.UserUpdater,
            token_processor: auth_interface.TokenProcessor,
    ) -> None:
        self._auth_gateway = auth_gateway
        self._token_processor = token_processor

    async def __call__(self, token) -> None:
        email = self._token_processor.verify_token(
            token, token_type=TokenType.ACCESS
        )
        await self._auth_gateway.update(email, {"is_verified": True})


class LoginInteractor:
    def __init__(
            self,
            auth_gateway: auth_interface.UserReader,
            token_processor: auth_interface.TokenProcessor,
    ) -> None:
        self._auth_gateway = auth_gateway
        self._token_processor = token_processor

    async def __call__(self, dto: auth_dto.LoginUserDTO) -> dict:
        user = await self._auth_gateway.get_by_email(dto.email)
        if user and user.is_verified:
            if not verify_password(dto.password, user.password):
                raise AuthenticationError
        else:
            raise AuthenticationError

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
            auth_gateway: auth_interface.UserReader,
            token_processor: auth_interface.TokenProcessor,
            email_gateway: email_interface.EmailSender,
            translations: dict[str, gettext.GNUTranslations],
    ) -> None:
        self._config = config
        self._auth_gateway = auth_gateway
        self._email_gateway = email_gateway
        self._token_processor = token_processor
        self._translations = translations

    async def __call__(self, email: str, language: str) -> None:
        user = await self._auth_gateway.get_by_email(email)
        if user:
            token = self._token_processor.create_password_reset_token(email)
            reset_link = f"{self._config.app.base_url}/reset-password?token={token}"
            # sending email
            if not (language in self._config.app.supported_languages):
                language = "en"
            _ = self._translations[language].gettext
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
            auth_gateway: auth_interface.UserUpdater,
            token_processor: auth_interface.TokenProcessor,
    ):
        self._auth_gateway = auth_gateway
        self._token_processor = token_processor

    async def __call__(self, token: str, password: str) -> None:
        email = self._token_processor.verify_token(
            token, token_type=TokenType.PASSWORD_RESET
        )
        hashed_password = hash_password(password)
        await self._auth_gateway.update(email, {"password": hashed_password})
