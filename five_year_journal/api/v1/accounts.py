from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.accounts import create_account
from ...dependencies import get_session
from ...schemas.accounts import AccountIn, AccountInResponse

accounts_router = APIRouter(prefix="/accounts", tags=["Accounts"])


@accounts_router.post(
    "/",
    response_model=AccountInResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    account: AccountIn, session: AsyncSession = Depends(get_session)
) -> AccountInResponse:
    """Create new account to use API."""
    return await create_account(session, account)
