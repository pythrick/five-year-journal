from datetime import datetime, timedelta

import jwt

from ..schemas.auth import AuthInResponse
from five_year_journal.config import settings


async def authenticate(email: str) -> AuthInResponse:
    access_token = jwt.encode(
        {
            "email": email,
            "exp": datetime.utcnow()
            + timedelta(seconds=settings.access_token_expiration_secs),
        },
        settings.api_secret.get_secret_value(),
        settings.jwt_algorithm,
    )
    refresh_token = jwt.encode(
        {
            "email": email,
            "exp": datetime.utcnow()
            + timedelta(seconds=settings.refresh_token_expiration_secs),
        },
        settings.api_secret.get_secret_value(),
        settings.jwt_algorithm,
    )
    return AuthInResponse(
        access_token=access_token, refresh_token=refresh_token
    )


async def refresh(email: str) -> str:
    return jwt.encode(
        {
            "email": email,
            "exp": datetime.utcnow()
            + timedelta(seconds=settings.access_token_expiration_secs),
        },
        settings.api_secret.get_secret_value(),
        settings.jwt_algorithm,
    )


async def validate_token(token: str) -> str:
    result = jwt.decode(
        token,
        settings.api_secret.get_secret_value(),
        settings.jwt_algorithm,
        options={"verify_exp": True},
    )
    return result["email"]
