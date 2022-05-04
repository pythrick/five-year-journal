from typing import Any, Callable, Coroutine

import pytest_asyncio
from faker import Faker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from five_year_journal.api import api
from five_year_journal.core.auth import authenticate
from five_year_journal.dependencies import get_session
from five_year_journal.models.accounts import Account
from five_year_journal.models.journal_logs import JournalLog


@pytest_asyncio.fixture(name="session")
async def session_fixture():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(name="client")
async def client_fixture(session: AsyncSession):
    async def get_session_override():
        yield session

    api.dependency_overrides[get_session] = get_session_override
    async with AsyncClient(
        app=api,
        base_url="http://test",
    ) as client:
        yield client
    api.dependency_overrides.clear()


@pytest_asyncio.fixture(name="auth_client")
async def auth_client_fixture(session: AsyncSession):
    async def get_auth_client(email: str):
        async def get_session_override():
            yield session

        api.dependency_overrides[get_session] = get_session_override
        auth = await authenticate(email)
        async with AsyncClient(
            app=api,
            base_url="http://test",
            headers={"Authorization": f"Bearer {auth.access_token}"},
        ) as client:
            yield client
        api.dependency_overrides.clear()

    return get_auth_client


@pytest_asyncio.fixture(name="account")
async def account_fixture(session: AsyncSession, faker: Faker) -> Account:
    data = Account(
        name=faker.name(),
        email=faker.email(),
        password=faker.pystr(),
        is_active=True,
        is_verified=False,
    )
    session.add(data)
    await session.commit()
    await session.refresh(data)
    return data


@pytest_asyncio.fixture(name="accounts_factory")
async def create_account(
    session: AsyncSession, faker: Faker
) -> Callable[
    [int, Account | None], Coroutine[Any, Any, list[Account | None]]
]:
    async def create(size: int, obj: Account = None):
        data = []
        for _ in range(size):
            item = obj or Account(
                name=faker.name(),
                email=faker.email(),
                password=faker.pystr(10),
                is_active=True,
                is_verified=False,
            )
            session.add(item)
            data.append(item)
        await session.commit()
        for item in data:
            await session.refresh(item)
        return data

    return create


@pytest_asyncio.fixture(name="journal_logs_factory")
async def create_journal_log(
    session: AsyncSession,
    faker: Faker,
    account: Account,
) -> Callable[
    [int, Account | None, JournalLog | None],
    Coroutine[Any, Any, list[JournalLog]],
]:
    async def create(
        size: int,
        account_obj: Account | None = account,
        obj: JournalLog = None,
    ):
        data = []
        for _ in range(size):
            item = obj or JournalLog(
                content=faker.sentence(),
                account_id=account_obj.id,
            )
            session.add(item)
            data.append(item)
        await session.commit()
        for item in data:
            await session.refresh(item)
        return sorted(data, key=lambda el: el.created_at, reverse=True)

    return create
