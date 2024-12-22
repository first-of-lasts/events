import gettext

from events.application.utils.security import verify_password, hash_password
from events.domain.exceptions.user import UserCannotBeCreatedError
from events.domain.exceptions.access import AuthenticationError
from events.infrastructure.auth.token import TokenType
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
        async with self._db_session.begin():
            # await self._db_session.acquire_lock("users", lock_mode="SHARE ROW EXCLUSIVE")
            await self._auth_gateway.delete_inactive_by_email(dto.email)

            # await self._db_session.acquire_lock("users", lock_mode="ROW SHARE")
            email_conflicts = await self._auth_gateway.exists_by_email(dto.email)
            if email_conflicts:
                raise UserCannotBeCreatedError("Email already exists")
            username_conflicts = await self._auth_gateway.exists_by_username(dto.username)
            if username_conflicts:
                raise UserCannotBeCreatedError("Username already exists")

            user = UserDM(
                email=dto.email,
                username=dto.username,
                password=hash_password(dto.password),
            )
            await self._auth_gateway.save(user)
        await self._send_verification_email(dto=dto, language=language)

    async def _send_verification_email(self, dto: auth_dto.NewUserDTO, language: str) -> None:
        # TODO try - translator = self._translations.get(language, gettext.NullTranslations())
        token = self._token_processor.create_access_token(dto.email)
        verification_link = f"{self._config.app.base_url}/verify-email?token={token}"
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
        if user and user.is_verified and user.is_active:
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
            await self._send_reset_email(email=email, language=language)

    async def _send_reset_email(self, email: str, language: str) -> None:
        token = self._token_processor.create_password_reset_token(email)
        reset_link = f"{self._config.app.base_url}/reset-password?token={token}"
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
