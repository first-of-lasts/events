from contextlib import asynccontextmanager

from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from events.main.config import Config
from events.presentation.http.routers.auth import auth_router
from events.presentation.http.routers.user import user_router
from events.presentation.http.routers.event import event_router
from events.main.ioc.providers import RootProvider, AuthProvider, UserProvider


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


def create_app() -> FastAPI:
    config = Config()
    docs = {} if config.app.debug else {"docs_url": None, "redoc_url": None, "openapi_url": None}
    _app = FastAPI(
        title=config.app.name, debug=config.app.debug, lifespan=lifespan, **docs
    )
    container = make_async_container(
        RootProvider(), AuthProvider(), UserProvider(),
        context={Config: config},
    )
    setup_dishka(container, _app)
    include_routers(_app)
    return _app


def include_routers(_app: FastAPI) -> None:
    _app.include_router(auth_router, prefix="/auth", tags=["auth", ])
    _app.include_router(user_router, prefix="/user", tags=["user", ])
    _app.include_router(event_router, prefix="/event", tags=["event", ])


app = create_app()
