import logging

from sqlalchemy import desc, extract
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from five_year_journal.models import JournalLog
from five_year_journal.schemas import JournalLogIn, JournalLogOut

logger = logging.getLogger(__name__)


async def create_journal_log(
    db_session: AsyncSession, journal_log_in: JournalLogIn
) -> JournalLogOut:
    journal_log = JournalLog(**journal_log_in.dict())
    db_session.add(journal_log)
    await db_session.commit()
    return JournalLogOut.from_orm(journal_log)


async def list_journal_logs(
    db_session: AsyncSession, day: int, month: int, limit: int, offset: int
) -> list[JournalLogOut]:
    statement = (
        select(JournalLog)
        .where(
            extract("day", JournalLog.created_at) == day
            and extract("month", JournalLogOut.created_at) == month
        )
        .limit(limit)
        .offset(offset)
        .order_by(desc(JournalLog.created_at))
    )
    result = await db_session.execute(statement)
    all_results = result.scalars()
    return [JournalLogOut.from_orm(item) for item in all_results]
