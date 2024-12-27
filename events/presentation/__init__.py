from fastapi import FastAPI

from events.domain.exceptions.base import DomainError
from events.presentation.http.routers.auth import auth_router
from events.presentation.http.routers.user import user_router
from events.presentation.http.routers.event import event_router
from events.presentation.http.routers.location import location_router
from events.presentation.http.exceptions import app_exception_handler


def include_routers(app: FastAPI) -> None:
    app.include_router(auth_router, prefix="/auth", tags=["auth", ])
    app.include_router(user_router, prefix="/user", tags=["user", ])
    app.include_router(location_router, prefix="/location", tags=["location", ])
    app.include_router(event_router, prefix="/event", tags=["event", ])


def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, app_exception_handler)
