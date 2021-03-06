from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, SecretStr, validator

BASE_PATH = Path(__file__).parent.parent.resolve()


class Settings(BaseSettings):
    database_url: SecretStr
    api_secret: SecretStr
    debug: bool = False
    access_token_expiration_secs: int = 60 * 60  # 1 hour
    refresh_token_expiration_secs: int = 60 * 60 * 24 * 180  # 6 months
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = BASE_PATH / ".env"

    @validator("database_url")
    def postgres_driver(cls, v: SecretStr):
        db_url = v.get_secret_value()
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+asyncpg://")
        return SecretStr(db_url)


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
