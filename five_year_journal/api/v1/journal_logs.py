from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from ...core.journal_logs import create_journal_log, list_journal_logs
from ...dependencies import get_current_account, get_session, get_token_header
from ...models.accounts import Account
from ...schemas.journal_logs import JournalLogIn, JournalLogInResponse

journal_logs_router = APIRouter(
    prefix="/journal-logs",
    tags=["Journal Logs"],
    dependencies=[Depends(get_token_header)],
)


@journal_logs_router.post(
    "/",
    response_model=JournalLogInResponse,
    status_code=status.HTTP_201_CREATED,
)
async def new_journal_log(
    journal_log: JournalLogIn,
    logged_account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_session),
):
    """Create new log entry in Journal."""
    response = await create_journal_log(session, journal_log, logged_account)
    return response


@journal_logs_router.get("/", response_model=list[JournalLogInResponse])
async def list_journal_logs_from_past_years(
    day: Optional[int] = Query(None),
    month: Optional[int] = Query(None),
    limit: int = Query(5),
    offset: int = Query(0),
    logged_account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_session),
):
    """List Journal Log entries for a day in the past years."""
    day = day or datetime.utcnow().day
    month = month or datetime.utcnow().month
    response = await list_journal_logs(
        session, logged_account, day, month, limit, offset
    )
    return response
