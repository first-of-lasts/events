from typing import List
from sqlalchemy import select, update, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from events.domain.models.event import EventDM#, EventListResponseDM
from events.application.interfaces import event_interface
from events.infrastructure.persistence.models import Event


class EventGateway(
    event_interface.EventCreator,
    event_interface.EventUpdater,
    event_interface.EventReader,
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

    async def update_event(self, user_id: int, event_id: int, update_data: dict) -> None:
        stmt = (
            update(Event)
            .where(Event.id == event_id, Event.user_id == user_id)
            .values(**update_data)
            .returning(Event)
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def list_user_events(
            self,
            user_id: int,
            sort_by: str,
            order: str,
            limit: int,
            offset: int,
            language: str,
    ) -> List[EventDM]:
        sort_column = getattr(Event, sort_by, Event.created_at)
        sort_order = desc(sort_column) if order == "desc" else asc(sort_column)
        stmt = (
            select(Event)
            .options(selectinload(Event.country), selectinload(Event.region))
            .where(Event.user_id == user_id)
            .order_by(sort_order)
            .offset(offset)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        events = result.scalars().all()
        # event_responses = [
        #     EventListResponseDM(
        #         id=event.id,
        #         title=event.title,
        #         description=event.description,
        #         country=event.country.get_name(language) if event.country else None,
        #         region=event.region.get_name(language) if event.region else None,
        #         created_at=event.created_at,
        #         updated_at=event.updated_at
        #     )
        #     for event in events
        # ]
        # return event_responses
