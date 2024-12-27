from events.application.interfaces import event_interface


class CreateEventInteractor:
    def __init__(
            self,
            event_gateway: event_interface.EventSaver,
    ) -> None:
        self._event_gateway = event_gateway

    async def __call__(self, email: str) -> None:
        return await self._event_gateway.save()
