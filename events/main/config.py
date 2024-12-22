from os import environ
from typing import List

from dotenv import load_dotenv
from pydantic import Field, BaseModel, AnyHttpUrl, field_validator

from events.infrastructure.auth.token import Algorithm


load_dotenv()


class AppConfig(BaseModel):
    name: str = Field(alias="APP_NAME", default="Events")
    debug: bool = Field(alias="APP_DEBUG", default=True)
    base_url: AnyHttpUrl = Field(alias="APP_BASE_URL", default="http://localhost:8000")
    jwt_secret: str = Field(alias="APP_JWT_SECRET", default="secret_key")
    jwt_secret_algorithm: Algorithm = Field(alias="APP_JWT_SECRET_ALGORITHM", default="HS256")
    supported_languages: List[str] = Field(alias="APP_SUPPORTED_LANGUAGES")

    @field_validator("supported_languages", mode="before")
    def parse_supported_languages(cls, v):
        if isinstance(v, str):
            return [lang.strip() for lang in v.split(',') if lang.strip()]
        elif isinstance(v, list):
            return v
        raise ValueError("APP_SUPPORTED_LANGUAGES must be a comma-separated string or a list of strings")

    class Config:
        extra = "ignore"


class PostgresConfig(BaseModel):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    user: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DATABASE")

    class Config:
        extra = "ignore"


class Config(BaseModel):
    app: AppConfig = Field(default_factory=lambda: AppConfig(**environ))
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**environ))


def get_postgres_uri(config: Config) -> str:
    return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
        host=config.postgres.host,
        port=config.postgres.port,
        user=config.postgres.user,
        password=config.postgres.password,
        database=config.postgres.database,
    )
