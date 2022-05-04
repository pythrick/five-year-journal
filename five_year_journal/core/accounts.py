from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..exceptions import InvalidCredentials, InvalidEmail
from ..helpers import verify_password
from ..models.accounts import Account
from ..schemas.accounts import AccountIn, AccountInResponse
from ..schemas.auth import AuthIn


async def create_account(
    db_session: AsyncSession, account_in: AccountIn
) -> AccountInResponse:
    account = Account(**account_in.dict())
    db_session.add(account)
    try:
        await db_session.commit()
    except IntegrityError as exc:
        raise InvalidEmail from exc
    return AccountInResponse.from_orm(account)


async def get_account_by_email(
    db_session: AsyncSession, email: str
) -> Account:
    statement = select(Account).where(Account.email == email)
    result = await db_session.execute(statement)
    account = result.scalar()
    if not account:
        raise InvalidCredentials("Client Account not found.")
    if not account.is_active:
        raise InvalidCredentials("Client Account inactive.")
    return account


async def validate_credentials(
    db_session: AsyncSession, credentials: AuthIn
) -> AccountInResponse:
    account = await get_account_by_email(db_session, credentials.email)
    if not verify_password(credentials.password, account.password):
        raise InvalidCredentials("Client Secret doesn't match.")
    return AccountInResponse(**account.dict())
