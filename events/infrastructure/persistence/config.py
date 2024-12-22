import os

from dotenv import load_dotenv


def load_supported_languages() -> list:
    load_dotenv()
    supported_languages_str = os.getenv("APP_SUPPORTED_LANGUAGES")
    supported_languages = [lang.strip() for lang in supported_languages_str.split(",") if lang.strip()]
    return supported_languages


def load_postgres_uri() -> str:
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    database = os.getenv("POSTGRES_DATABASE")
    return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )
