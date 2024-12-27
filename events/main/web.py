from contextlib import asynccontextmanager
from fastapi import FastAPI

from events import presentation
from events.main import ioc
from events.main.config import Config


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


def create_app(config: Config) -> FastAPI:
    docs = {} if config.app.debug else {"docs_url": None, "redoc_url": None, "openapi_url": None}
    _app = FastAPI(
        title=config.app.name, debug=config.app.debug, lifespan=lifespan, **docs
    )
    ioc.setup(_app, config)
    presentation.include_routers(_app)
    presentation.include_exception_handlers(_app)
    return _app


app = create_app(config=Config())
