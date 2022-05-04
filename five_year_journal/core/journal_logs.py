from sqlalchemy import and_, desc, extract
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.accounts import Account
from ..models.journal_logs import JournalLog
from ..schemas.journal_logs import JournalLogIn, JournalLogInResponse


async def create_journal_log(
    db_session: AsyncSession, journal_log_in: JournalLogIn, account: Account
) -> JournalLogInResponse:
    journal_log = JournalLog(**journal_log_in.dict(), account_id=account.id)
    db_session.add(journal_log)
    await db_session.commit()
    return JournalLogInResponse.from_orm(journal_log)


async def list_journal_logs(
    db_session: AsyncSession,
    account: Account,
    day: int,
    month: int,
    limit: int,
    offset: int,
) -> list[JournalLogInResponse]:
    statement = (
        select(JournalLog)
        .where(
            and_(
                JournalLog.account_id == account.id,
                extract("day", JournalLog.created_at) == day,
                extract("month", JournalLog.created_at) == month,
            )
        )
        .limit(limit)
        .offset(offset)
        .order_by(desc(JournalLog.created_at))
    )
    result = await db_session.execute(statement)
    all_results = result.scalars()
    return [JournalLogInResponse.from_orm(item) for item in all_results]
