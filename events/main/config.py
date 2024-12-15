from os import environ
from typing import Tuple

from dotenv import load_dotenv
from pydantic import Field, BaseModel, AnyHttpUrl

from events.infrastructure.adapters.auth.token import Algorithm


load_dotenv()


class AppConfig(BaseModel):
    name: str = Field(alias="APP_NAME", default="Events")
    debug: bool = Field(alias="APP_DEBUG", default=True)
    base_url: AnyHttpUrl = Field(alias="APP_BASE_URL", default="http://localhost:8000")
    jwt_secret: str = Field(alias="APP_JWT_SECRET", default="secret_key")
    jwt_secret_algorithm: Algorithm = Field(alias="APP_JWT_SECRET_ALGORITHM", default="HS256")
    supported_languages: Tuple[str] = ("uz", "ru", "en")

    class Config:
        extra = "ignore"


class PostgresConfig(BaseModel):
    host: str = Field(alias="POSTGRES_HOST", default="localhost")
    port: int = Field(alias="POSTGRES_PORT", default=5432)
    login: str = Field(alias="POSTGRES_USER", default="postgres")
    password: str = Field(alias="POSTGRES_PASSWORD", default="postgres")
    database: str = Field(alias="POSTGRES_DB", default="events")

    class Config:
        extra = "ignore"


class Config(BaseModel):
    app: AppConfig = Field(default_factory=lambda: AppConfig(**environ))
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**environ))


def get_postgres_uri(config: Config) -> str:
    return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
        host=config.postgres.host,
        port=config.postgres.port,
        user=config.postgres.login,
        password=config.postgres.password,
        db=config.postgres.database,
    )
