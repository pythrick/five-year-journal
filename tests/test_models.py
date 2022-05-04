from typing import Any, Callable, Coroutine

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from five_year_journal.models.accounts import Account
from five_year_journal.models.journal_logs import JournalLog


async def test_list_journal_log_model(
    session: AsyncSession,
    account: Account,
    journal_logs_factory: Callable[
        [int, Account], Coroutine[Any, Any, list[JournalLog]]
    ],
):
    journal_logs = await journal_logs_factory(10, account)

    stmt = select(JournalLog).order_by(desc(JournalLog.created_at))
    result = await session.execute(stmt)
    for journal_log, (item,) in zip(journal_logs, result.all()):
        assert item == journal_log


async def test_insert_account_model(
    session: AsyncSession,
    accounts_factory: Callable[
        [int], Coroutine[Any, Any, list[Account | None]]
    ],
):
    account = (await accounts_factory(1))[0]
    stmt = select(Account).where(Account.email == account.email)
    result = await session.execute(stmt)
    inserted_account = result.one_or_none()[0]
    assert inserted_account == account


async def test_hash_password():
    result = Account.hash_password("test")
    assert result != "test"
