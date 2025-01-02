from dishka import Provider, provide, Scope, AnyOf

from events.application.interfaces import attendee_interface
from events.application.interactors import attendee_interactor
from events.infrastructure.gateways.attendee_gateway import AttendeeGateway


class AttendeeProvider(Provider):
    attendee_gateway = provide(
        source=AttendeeGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            attendee_interface.AttendeeCreator,
        ]
    )

    @provide(scope=Scope.REQUEST)
    def create_attendee_interactor(
            self,
            attendee_gateway: attendee_interface.AttendeeCreator,
    ) -> attendee_interactor.CreateAttendeeInteractor:
        return attendee_interactor.CreateAttendeeInteractor(
            attendee_gateway=attendee_gateway,
        )
