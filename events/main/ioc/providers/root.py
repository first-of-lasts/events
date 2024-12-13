from datetime import timedelta
from typing import AsyncIterable
from dishka import Provider, Scope, provide, AnyOf, from_context
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, \
    AsyncEngine, create_async_engine

from events.infrastructure.adapters.auth.token import JwtTokenProcessor
from events.infrastructure.gateways.email_gateway import MockEmailGateway, EmailGateway
from events.application.interfaces import email_interface
from events.application.interfaces import root_interface
from events.infrastructure.adapters.database.manager import new_session_maker
from events.main.config import Config, get_postgres_uri


class RootProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(get_postgres_uri(config))

    @provide(scope=Scope.APP)
    def email_gateway(self, config: Config) -> email_interface.EmailSender:
        if config.app.debug:
            return MockEmailGateway()
        else:
            return EmailGateway(
                smtp_server=config.smtp.server,
                smtp_port=config.smtp.port,
                username=config.smtp.username,
                password=config.smtp.password,
            )

    @provide(scope=Scope.APP)
    def jwt_token_processor(self, config: Config) -> JwtTokenProcessor:
        return JwtTokenProcessor(
            secret=config.app.jwt_secret,
            access_token_expires=timedelta(minutes=15),
            refresh_token_expires=timedelta(days=7),
            algorithm=config.app.jwt_secret_algorithm,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AnyOf[
        AsyncSession,
        root_interface.DBSession,
    ]]:
        async with session_maker() as session:
            yield session
