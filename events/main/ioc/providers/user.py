from dishka import Provider, provide, Scope, AnyOf

from events.application.interactors import user_interactor
from events.infrastructure.gateways.user_gateway import UserGateway
from events.application.interfaces import user_interface, location_interface



class UserProvider(Provider):
    user_gateway = provide(
        source=UserGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            user_interface.UserReader, user_interface.UserUpdater,
        ]
    )

    @provide(scope=Scope.REQUEST)
    def get_current_user_interactor(
            self,
            user_gateway: user_interface.UserReader,
    ) -> user_interactor.GetCurrentUserInteractor:
        return user_interactor.GetCurrentUserInteractor(
            user_gateway=user_gateway,
        )

    @provide(scope=Scope.REQUEST)
    def update_current_user_interactor(
            self,
            user_gateway: user_interface.UserUpdater,
            location_gateway: location_interface.CountryReader and location_interface.RegionReader,
    ) -> user_interactor.UpdateCurrentUserInteractor:
        return user_interactor.UpdateCurrentUserInteractor(
            user_gateway=user_gateway,
            location_gateway=location_gateway,
        )
