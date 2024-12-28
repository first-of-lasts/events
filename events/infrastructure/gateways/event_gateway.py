from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from events.domain.models.event import EventDM
from events.application.interfaces import event_interface
from events.infrastructure.persistence.models import Event


class EventGateway(
    event_interface.EventSaver
):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, event: EventDM) -> None:
        new_event = Event(
            title=event.title,
            description=event.description,
            country_id=event.country
        )
        self._session.add(new_event)
        # new_user = User(
        #     email=user.email,
        #     username=user.username,
        #     password=user.password,
        # )
        # self._session.add(new_user)
