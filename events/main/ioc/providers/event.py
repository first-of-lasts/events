from dishka import Provider, provide, Scope, AnyOf

from events.application.interfaces import event_interface
from events.application.interfaces import user_interface
from events.application.interactors import event_interactor
from events.application.services.location_validator import LocationValidator
from events.infrastructure.gateways.event_gateway import EventGateway


class EventProvider(Provider):
    event_gateway = provide(
        source=EventGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            event_interface.EventCreator,
            event_interface.EventUpdater,
            event_interface.EventReader,
            event_interface.EventDeleter,
            event_interface.CategoryReader,
        ]
    )

    @provide(scope=Scope.REQUEST)
    def create_event_interactor(
            self,
            event_gateway: event_interface.EventCreator,
            location_validator: LocationValidator,
    ) -> event_interactor.CreateEventInteractor:
        return event_interactor.CreateEventInteractor(
            event_gateway=event_gateway,
            location_validator=location_validator,
        )

    @provide(scope=Scope.REQUEST)
    def update_event_interactor(
            self,
            event_gateway: event_interface.EventUpdater,
            location_validator: LocationValidator,
    ) -> event_interactor.UpdateEventInteractor:
        return event_interactor.UpdateEventInteractor(
            event_gateway=event_gateway,
            location_validator=location_validator,
        )

    @provide(scope=Scope.REQUEST)
    def list_user_events_interactor(
            self,
            event_gateway: event_interface.EventReader,
    ) -> event_interactor.ListUserEventsInteractor:
        return event_interactor.ListUserEventsInteractor(
            event_gateway=event_gateway,
        )

    @provide(scope=Scope.REQUEST)
    def list_recommended_events_interactor(
            self,
            event_gateway: event_interface.EventReader,
            user_gateway: user_interface.UserReader,
    ) -> event_interactor.ListRecommendedEventsInteractor:
        return event_interactor.ListRecommendedEventsInteractor(
            event_gateway=event_gateway,
            user_gateway=user_gateway,
        )

    @provide(scope=Scope.REQUEST)
    def delete_event_interactor(
            self,
            event_gateway: event_interface.EventDeleter,
    ) -> event_interactor.DeleteEventInteractor:
        return event_interactor.DeleteEventInteractor(
            event_gateway=event_gateway,
        )

    @provide(scope=Scope.REQUEST)
    def list_categories_interactor(
            self,
            event_gateway: event_interface.CategoryReader,
    ) -> event_interactor.ListCategoriesInteractor:
        return event_interactor.ListCategoriesInteractor(
            event_gateway=event_gateway,
        )


