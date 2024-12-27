from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from events.main.config import Config
from events.main.ioc.providers.root import RootProvider
from events.main.ioc.providers.auth import AuthProvider
from events.main.ioc.providers.location import LocationProvider
from events.main.ioc.providers.user import UserProvider


def setup(app: FastAPI, config: Config):
    container = make_async_container(
        RootProvider(), AuthProvider(), UserProvider(), LocationProvider(),
        context={Config: config},
    )
    setup_dishka(container, app)
