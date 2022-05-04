from fastapi import APIRouter, Depends
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from five_year_journal.core import auth
from five_year_journal.core.accounts import (
    get_account_by_email,
    validate_credentials,
)
from five_year_journal.core.auth import validate_token
from five_year_journal.dependencies import get_session
from five_year_journal.exceptions import (
    InvalidCredentials,
    InvalidToken,
    Unauthorized,
)
from five_year_journal.schemas.auth import (
    AuthIn,
    AuthInResponse,
    RefreshIn,
    RefreshInResponse,
)

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/token", response_model=AuthInResponse)
async def authenticate(
    credentials: AuthIn, session: AsyncSession = Depends(get_session)
) -> AuthInResponse:
    """Generate authentication tokens."""
    try:
        await validate_credentials(session, AuthIn(**credentials.dict()))
        response = await auth.authenticate(credentials.email)
    except InvalidCredentials as exc:
        raise Unauthorized("Invalid credentials") from exc
    return response


@auth_router.post("/refresh", response_model=RefreshInResponse)
async def refresh(
    data: RefreshIn, session: AsyncSession = Depends(get_session)
) -> RefreshInResponse:
    """Refresh access_token."""
    try:
        email = await validate_token(data.refresh_token)
    except InvalidTokenError as exc:
        raise InvalidToken from exc
    client_account = await get_account_by_email(session, email)
    refreshed_access_token = await auth.refresh(client_account.email)
    return RefreshInResponse(
        access_token=refreshed_access_token, refresh_token=data.refresh_token
    )
