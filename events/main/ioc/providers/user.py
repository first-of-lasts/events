import gettext

from dishka import Provider, provide, Scope, AnyOf

from events.application.interactors.user_interactor import GetUserInteractor, UpdateUserInteractor
from events.infrastructure.gateways.user_gateway import UserGateway
from events.application.interfaces import user_interface



class UserProvider(Provider):
    user_gateway = provide(
        source=UserGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            user_interface.UserReader, user_interface.UserUpdater,
        ]
    )

    @provide(scope=Scope.REQUEST)
    def get_user_interactor(
            self,
            user_gateway: user_interface.UserReader,
            #translations: dict[str, gettext.GNUTranslations],
    ) -> GetUserInteractor:
        return GetUserInteractor(
            user_gateway=user_gateway,
            #translations=translations
        )

    @provide(scope=Scope.REQUEST)
    def update_user_interactor(
            self,
            user_gateway: user_interface.UserUpdater
    ) -> UpdateUserInteractor:
        return UpdateUserInteractor(
            user_gateway=user_gateway,
        )
