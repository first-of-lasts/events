from fastapi import FastAPI

from events.domain.exceptions.base import DomainError
from events.presentation.http.routers.auth import auth_router
from events.presentation.http.routers.user import user_router
from events.presentation.http.routers.event import event_router
from events.presentation.http.routers.attendee import attendee_router
from events.presentation.http.routers.location import location_router
from events.presentation.http.exceptions import app_exception_handler


def include_routers(app: FastAPI) -> None:
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth", ])
    app.include_router(user_router, prefix="/api/v1/users", tags=["user", ])
    app.include_router(location_router, prefix="/api/v1/locations", tags=["location", ])
    app.include_router(event_router, prefix="/api/v1/events", tags=["event", ])
    app.include_router(attendee_router, prefix="/api/v1/attendees", tags=["attendee", ])


def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, app_exception_handler)
