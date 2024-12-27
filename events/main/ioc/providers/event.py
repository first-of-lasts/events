from dishka import Provider, provide, Scope, AnyOf

from events.application.interfaces import event_interface
from events.application.interactors import event_interactor
from events.infrastructure.gateways.event_gateway import EventGateway


class EventProvider(Provider):
    location_gateway = provide(
        source=EventGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            event_interface.EventSaver,
        ]
    )

    @provide(scope=Scope.REQUEST)
    def create_event_interactor(
            self,
            event_gateway: event_interface.EventSaver,
    ) -> event_interactor.CreateEventInteractor:
        return event_interactor.CreateEventInteractor(
            event_gateway=event_gateway
        )
