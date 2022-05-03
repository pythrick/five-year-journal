from functools import lru_cache
from pathlib import Path

from pydantic import AnyUrl, BaseSettings, PostgresDsn

BASE_PATH = Path(__file__).parent.resolve()


class DatabaseDsn(AnyUrl):
    allowed_schemes = PostgresDsn.allowed_schemes | {
        "sqlite",
        "sqlite+aiosqlite",
    }
    host_required = False


class Settings(BaseSettings):
    database_dsn: DatabaseDsn
    debug: bool = False

    class Config:
        env_file = BASE_PATH / ".env"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
