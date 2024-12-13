from datetime import datetime
from sqlalchemy import MetaData, Integer, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import as_declarative, Mapped, mapped_column
from sqlalchemy.sql import func


def new_session_maker(database_uri) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        database_uri,
        echo=False,
    )
    return async_sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )


POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


@as_declarative(metadata=metadata)
class Base:
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # @declared_attr
    # def __tablename__(cls) -> str:
    #    return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()

    # def __repr__(self) -> str:
    #     pk = inspect(self.__class__).primary_key[0].name
    #     return f'<{self.__class__.__name__} {getattr(self, pk, id(self))}>'
