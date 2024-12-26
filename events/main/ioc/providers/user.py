from dishka import Provider, provide, Scope, AnyOf

from events.application.interactors import user_interactor
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
    ) -> user_interactor.GetUserInteractor:
        return user_interactor.GetUserInteractor(
            user_gateway=user_gateway,
        )

    @provide(scope=Scope.REQUEST)
    def update_user_interactor(
            self,
            user_gateway: user_interface.UserUpdater
    ) -> user_interactor.UpdateUserInteractor:
        return user_interactor.UpdateUserInteractor(
            user_gateway=user_gateway,
        )
