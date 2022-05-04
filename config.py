from functools import lru_cache
from pathlib import Path

from pydantic import AnyUrl, BaseSettings, PostgresDsn, SecretStr

BASE_PATH = Path(__file__).parent.resolve()


class DatabaseDsn(AnyUrl):
    allowed_schemes = PostgresDsn.allowed_schemes | {
        "sqlite",
        "sqlite+aiosqlite",
    }
    host_required = False


class Settings(BaseSettings):
    database_dsn: DatabaseDsn
    api_secret: SecretStr
    debug: bool = False
    access_token_expiration_secs: int = 60 * 60  # 1 hour
    refresh_token_expiration_secs: int = 60 * 60 * 24 * 180  # 6 months
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = BASE_PATH / ".env"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
