from fastapi import FastAPI
from dishka import make_async_container, Provider
from dishka.integrations.fastapi import setup_dishka

from events.main.config import Config
from events.main.ioc.providers.root import RootProvider
from events.main.ioc.providers.auth import AuthProvider
from events.main.ioc.providers.user import UserProvider
from events.main.ioc.providers.location import LocationProvider
from events.main.ioc.providers.event import EventProvider
from events.main.ioc.providers.attendee import AttendeeProvider


def get_providers() -> list[Provider]:
    providers = [
        RootProvider(),
        AuthProvider(),
        UserProvider(),
        LocationProvider(),
        EventProvider(),
        AttendeeProvider(),
    ]
    return providers


def setup(app: FastAPI, config: Config):
    providers = get_providers()
    container = make_async_container(
        *providers, context={Config: config},
    )
    setup_dishka(container, app)
