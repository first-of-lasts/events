from contextlib import asynccontextmanager

from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from events import presentation
from events.main.config import Config
from events.main.ioc.providers import RootProvider, AuthProvider, UserProvider


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


def create_app(config: Config) -> FastAPI:
    docs = {} if config.app.debug else {"docs_url": None, "redoc_url": None, "openapi_url": None}
    _app = FastAPI(
        title=config.app.name, debug=config.app.debug, lifespan=lifespan, **docs
    )
    container = make_async_container(
        RootProvider(), AuthProvider(), UserProvider(),
        context={Config: config},
    )
    setup_dishka(container, _app)
    presentation.include_routers(_app)
    presentation.include_exception_handlers(_app)
    return _app


app = create_app(config=Config())
