from sqlalchemy import MetaData, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import as_declarative, Mapped, mapped_column


def new_session_maker(database_uri) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        database_uri,
        echo=False,
    )
    return async_sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )


@as_declarative(metadata=MetaData())
class Base:
    __abstract__ = True
