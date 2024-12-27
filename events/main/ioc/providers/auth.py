import gettext
from datetime import timedelta
from dishka import Provider, Scope, provide, AnyOf

from events.application.interfaces import root_interface
from events.application.interfaces import auth_interface
from events.application.interfaces import email_interface
from events.application.interactors import auth_interactor
from events.infrastructure.auth.token import JwtTokenProcessor
from events.infrastructure.gateways.auth_gateway import AuthGateway
from events.main.config import Config


class AuthProvider(Provider):
    auth_gateway = provide(
        source=AuthGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            auth_interface.UserSaver, auth_interface.UserUpdater, auth_interface.UserReader, auth_interface.TokenProcessor
        ]
    )

    @provide(scope=Scope.APP)
    def jwt_token_processor(self, config: Config) -> JwtTokenProcessor:
        return JwtTokenProcessor(
            secret=config.app.jwt_secret,
            access_token_expires=timedelta(hours=1),
            refresh_token_expires=timedelta(days=7),
            algorithm=config.app.jwt_secret_algorithm,
        )

    @provide(scope=Scope.REQUEST)
    def register_interactor(
        self,
        config: Config,
        db_session: root_interface.DBSession,
        auth_gateway: auth_interface.UserSaver,
        email_gateway: email_interface.EmailSender,
        token_processor: auth_interface.TokenProcessor,
        translations: dict[str, gettext.GNUTranslations],
    ) -> auth_interactor.RegisterInteractor:
        return auth_interactor.RegisterInteractor(
            config=config,
            db_session=db_session,
            auth_gateway=auth_gateway,
            email_gateway=email_gateway,
            token_processor=token_processor,
            translations=translations,
        )

    @provide(scope=Scope.REQUEST)
    def verify_interactor(
            self,
            auth_gateway: auth_interface.UserUpdater,
            token_processor: auth_interface.TokenProcessor,
    ) -> auth_interactor.VerifyInteractor:
        return auth_interactor.VerifyInteractor(
            auth_gateway=auth_gateway,
            token_processor=token_processor,
        )

    @provide(scope=Scope.REQUEST)
    def login_interactor(
            self,
            auth_gateway: auth_interface.UserReader,
            token_processor: auth_interface.TokenProcessor,
    ) -> auth_interactor.LoginInteractor:
        return auth_interactor.LoginInteractor(
            auth_gateway=auth_gateway,
            token_processor=token_processor,
        )

    @provide(scope=Scope.REQUEST)
    def password_reset_interactor(
            self,
            config: Config,
            auth_gateway: auth_interface.UserReader,
            email_gateway: email_interface.EmailSender,
            token_processor: auth_interface.TokenProcessor,
            translations: dict[str, gettext.GNUTranslations],
    ) -> auth_interactor.PasswordResetInteractor:
        return auth_interactor.PasswordResetInteractor(
            config=config,
            auth_gateway=auth_gateway,
            email_gateway=email_gateway,
            token_processor=token_processor,
            translations=translations,
        )

    @provide(scope=Scope.REQUEST)
    def password_reset_confirm_interactor(
            self,
            auth_gateway: auth_interface.UserUpdater,
            token_processor: auth_interface.TokenProcessor,
    ) -> auth_interactor.PasswordResetConfirmInteractor:
        return auth_interactor.PasswordResetConfirmInteractor(
            auth_gateway=auth_gateway,
            token_processor=token_processor,
        )

    @provide(scope=Scope.REQUEST)
    def create_token_pair_interactor(
            self,
            token_processor: auth_interface.TokenProcessor,
    ) -> auth_interactor.CreateTokenPairInteractor:
        return auth_interactor.CreateTokenPairInteractor(
            token_processor=token_processor,
        )
