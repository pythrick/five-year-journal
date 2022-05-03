from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from five_year_journal.models import JournalLog


async def test_insert_job_log_model(session: AsyncSession):
    stmt = select(JournalLog).where(JournalLog.content == "xxxx")
    result = await session.execute(stmt)
    assert result.one_or_none() is None
    data = JournalLog(content="xxxx")
    session.add(data)
    await session.commit()

    stmt = select(JournalLog).where(JournalLog.content == "xxxx")
    result = await session.execute(stmt)
    assert result.one_or_none()[0].content == data.content


async def test_list_job_log_model(session: AsyncSession):
    for i in range(10):
        session.add(JournalLog(content=f"content_{i}"))
    await session.commit()

    stmt = select(JournalLog).order_by(JournalLog.created_at)
    result = await session.execute(stmt)
    for i, (item,) in zip(range(10), result.all()):
        assert item.content == f"content_{i}"
