from dishka import Provider, provide, Scope, AnyOf

from events.application.interfaces import event_interface, user_interface, location_interface
from events.application.interactors import event_interactor
from events.infrastructure.gateways.event_gateway import EventGateway


class EventProvider(Provider):
    event_gateway = provide(
        source=EventGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            event_interface.EventCreator,
        ]
    )

    @provide(scope=Scope.REQUEST)
    def create_event_interactor(
            self,
            event_gateway: event_interface.EventCreator,
            user_gateway: user_interface.UserReader,
            location_gateway: location_interface.CountryReader and location_interface.RegionReader,
    ) -> event_interactor.CreateEventInteractor:
        return event_interactor.CreateEventInteractor(
            event_gateway=event_gateway,
            user_gateway=user_gateway,
            location_gateway=location_gateway,
        )
