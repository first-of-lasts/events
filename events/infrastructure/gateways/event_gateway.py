from typing import List
from sqlalchemy import select, update, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from events.domain.models.event import EventDM
from events.domain.exceptions.access import ActionPermissionError
from events.domain.exceptions.event import EventNotFoundError
from events.application.interfaces import event_interface
from events.application.schemas.responses import event_response
from events.infrastructure.persistence.models import Event


class EventGateway(
    event_interface.EventCreator,
    event_interface.EventUpdater,
    event_interface.EventReader,
    event_interface.EventDeleter,
):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_event(self, event: EventDM) -> None:
        new_event = Event(
            user_id=event.user_id,
            title=event.title,
            description=event.description,
            starts_at=event.starts_at,
            ends_at=event.ends_at,
            country_id=event.country_id,
            region_id=event.region_id,
        )
        self._session.add(new_event)
        await self._session.commit()

    async def update_event(self, user_id: int, event_id: int, update_data: dict) -> None:
        result = await self._session.execute(
            select(Event)
            .where(Event.id == event_id, Event.is_deleted == False)
        )
        event = result.scalars().one_or_none()
        if not event:
            raise EventNotFoundError(f"Event not found")
        if event.is_occurred:
            raise ActionPermissionError("Event can not be updated")
        if event.user_id != user_id:
            raise ActionPermissionError("You can not update this event")

        await self._session.execute(
            update(Event)
            .where(Event.id == event_id, Event.user_id == user_id)
            .values(**update_data)
        )
        await self._session.commit()

    async def get_user_events_list(
            self,
            user_id: int,
            sort_by: str,
            order: str,
            limit: int,
            offset: int,
            language: str,
    ) -> List[event_response.UserEventList]:
        sort_column = getattr(Event, sort_by, Event.created_at)
        sort_order = desc(sort_column) if order == "desc" else asc(sort_column)
        stmt = (
            select(Event)
            .options(selectinload(Event.country), selectinload(Event.region))
            .where(Event.user_id == user_id, Event.is_deleted == False)
            .order_by(sort_order)
            .offset(offset)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        events = result.scalars().all()
        event_responses = [
            event_response.UserEventList(
                id=event.id,
                title=event.title,
                description=event.description,
                starts_at=event.starts_at,
                ends_at=event.ends_at,
                is_occurred=event.is_occurred,
                country=event.country.get_name(language) if event.country else None,
                region=event.region.get_name(language) if event.region else None,
            )
            for event in events
        ]
        return event_responses

    async def delete_event(self, event_id: int, user_id: int) -> None:
        result = await self._session.execute(
            select(Event)
            .where(Event.id == event_id, Event.is_deleted == False)
        )
        event = result.scalars().one_or_none()
        if not event:
            raise EventNotFoundError(f"Event not found")
        if event.user_id != user_id:
            raise ActionPermissionError("You are not authorized to delete this event")

        await self._session.execute(
            update(Event)
            .where(Event.id == event_id)
            .values(is_deleted=True)
        )
        await self._session.commit()
