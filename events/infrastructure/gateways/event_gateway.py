from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from events.domain.models.event import EventDM
from events.application.interfaces import event_interface
from events.infrastructure.persistence.models import Event


class EventGateway(
    event_interface.EventCreator
):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_event(self, event: EventDM) -> None:
        new_event = Event(
            user_id=event.user_id,
            title=event.title,
            description=event.description,
            country_id=event.country_id,
            region_id=event.region_id,
        )
        self._session.add(new_event)
        await self._session.commit()
