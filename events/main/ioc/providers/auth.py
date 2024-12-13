from dishka import Provider, Scope, provide, AnyOf

from events.application.interactors.auth_interactor import \
    PasswordResetInteractor, PasswordResetConfirmInteractor
from events.infrastructure.adapters.auth.token import JwtTokenProcessor
from events.application.interfaces import auth_interface
from events.application.interfaces import email_interface
from events.infrastructure.gateways.auth_gateway import AuthGateway
from events.application.interactors.auth_interactor import RegisterInteractor, \
    VerifyInteractor, LoginInteractor


class AuthProvider(Provider):
    auth_gateway = provide(
        source=AuthGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            auth_interface.UserSaver, auth_interface.UserUpdater, auth_interface.UserReader,
        ]
    )

    @provide(scope=Scope.REQUEST)
    def register_interactor(
        self,
        auth_gateway: auth_interface.UserSaver,
        email_gateway: email_interface.EmailSender,
        jwt_token_processor: JwtTokenProcessor,
    ) -> RegisterInteractor:
        return RegisterInteractor(
            auth_gateway=auth_gateway,
            email_gateway=email_gateway,
            jwt_token_processor=jwt_token_processor,
        )

    @provide(scope=Scope.REQUEST)
    def verify_interactor(
            self,
            auth_gateway: auth_interface.UserUpdater,
            jwt_token_processor: JwtTokenProcessor,
    ) -> VerifyInteractor:
        return VerifyInteractor(
            auth_gateway=auth_gateway,
            jwt_token_processor=jwt_token_processor
        )

    @provide(scope=Scope.REQUEST)
    def login_interactor(
            self,
            auth_gateway: auth_interface.UserReader,
            jwt_token_processor: JwtTokenProcessor,
    ) -> LoginInteractor:
        return LoginInteractor(
            auth_gateway=auth_gateway,
            jwt_token_processor=jwt_token_processor
        )

    @provide(scope=Scope.REQUEST)
    def password_reset_interactor(
            self,
            auth_gateway: auth_interface.UserReader,
            email_gateway: email_interface.EmailSender,
            jwt_token_processor: JwtTokenProcessor,
    ) -> PasswordResetInteractor:
        return PasswordResetInteractor(
            auth_gateway=auth_gateway,
            email_gateway=email_gateway,
            jwt_token_processor=jwt_token_processor,
        )

    @provide(scope=Scope.REQUEST)
    def password_reset_confirm_interactor(
            self,
            auth_gateway: auth_interface.UserUpdater,
            jwt_token_processor: JwtTokenProcessor,
    ) -> PasswordResetConfirmInteractor:
        return PasswordResetConfirmInteractor(
            auth_gateway=auth_gateway,
            jwt_token_processor=jwt_token_processor,
        )
