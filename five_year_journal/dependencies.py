from typing import AsyncGenerator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from .core.accounts import get_account_by_email
from .core.auth import validate_token
from .db import engine
from .exceptions import InvalidToken


async def get_session() -> AsyncGenerator[AsyncSession, AsyncSession]:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


async def get_token_header(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    if not credentials:
        raise InvalidToken
    try:
        await validate_token(credentials.credentials)
    except InvalidTokenError as exc:
        raise InvalidToken from exc
    return True


async def get_current_account(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    session: AsyncSession = Depends(get_session),
):
    email = await validate_token(credentials.credentials)
    account = await get_account_by_email(session, email)
    return account
