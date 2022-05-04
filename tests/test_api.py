from datetime import datetime, timedelta
from typing import Any, AsyncGenerator, Callable, Coroutine
from uuid import UUID

import pytest
from fastapi import status
from httpx import AsyncClient

from five_year_journal.models.accounts import Account
from five_year_journal.models.journal_logs import JournalLog


async def test_new_account_v1(client: AsyncClient, faker):
    data = {
        "name": faker.name(),
        "email": faker.email(),
        "password": faker.pystr(),
    }
    response = await client.post("/v1/accounts/", json=data)
    result = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert result["name"] == data["name"]
    assert result["email"] == data["email"]
    assert result["id"] is not None
    assert "password" not in result


async def test_new_journal_log_v1(
    auth_client: Callable[[str], AsyncGenerator[AsyncClient, None]],
    account: Account,
):
    client = await anext(auth_client(account.email))
    response = await client.post(
        "/v1/journal-logs/", json={"content": "yyyyy"}
    )
    result = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert len(result["id"]) == 36
    assert UUID(result["id"])
    assert result["content"] == "yyyyy"
    assert result["updatedAt"] is None
    assert (
        datetime.utcnow() - datetime.fromisoformat(result["createdAt"])
    ).total_seconds() < 1


async def test_new_journal_log_v1_without_authentication(
    client: AsyncClient,
):
    response = await client.post(
        "/v1/journal-logs/", json={"content": "yyyyy"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_list_journal_logs_v1_without_authentication(
    client: AsyncClient,
):
    response = await client.get("/v1/journal-logs/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "records_created,limit,offset,results",
    (
        (5, 5, 0, 5),
        (10, 5, 0, 5),
        (10, 10, 0, 10),
        (10, 5, 2, 5),
        (2, 5, 2, 0),
    ),
)
async def test_list_journal_logs_v1(
    auth_client: Callable[[str], AsyncGenerator[AsyncClient, None]],
    account: Account,
    journal_logs_factory: Callable[
        [int, Account], Coroutine[Any, Any, list[JournalLog]]
    ],
    records_created: int,
    limit: int,
    offset: int,
    results: int,
):
    journal_logs = await journal_logs_factory(records_created, account)
    client = await anext(auth_client(account.email))
    response = await client.get(
        "/v1/journal-logs/", params={"limit": limit, "offset": offset}
    )
    result = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(result) == results

    for result_item, journal_log in zip(
        result, journal_logs[offset : offset + limit]
    ):
        assert UUID(result_item["id"]) == journal_log.id
        assert result_item["content"] == journal_log.content
        assert (
            journal_log.created_at
            - datetime.fromisoformat(result_item["createdAt"])
        ).total_seconds() < 1
        assert result_item["updatedAt"] is None


async def test_list_journal_logs_v1_should_not_return_from_another_accounts(
    auth_client: Callable[[str], AsyncGenerator[AsyncClient, None]],
    account: Account,
    accounts_factory: Callable[
        [int], Coroutine[Any, Any, list[Account | None]]
    ],
    journal_logs_factory: Callable[
        [int, Account], Coroutine[Any, Any, list[JournalLog]]
    ],
):
    random_accounts = await accounts_factory(5)
    for random_account in random_accounts:
        await journal_logs_factory(3, random_account)

    client = await anext(auth_client(account.email))
    response = await client.get("/v1/journal-logs/")
    result = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(result) == 0


async def test_list_journal_logs_v1_dont_return_results_from_another_date(
    auth_client: Callable[[str], AsyncGenerator[AsyncClient, None]],
    account: Account,
    journal_logs_factory: Callable[
        [int, Account], Coroutine[Any, Any, list[JournalLog]]
    ],
):
    await journal_logs_factory(2, account)
    client = await anext(auth_client(account.email))
    search_date = datetime.utcnow() + timedelta(days=2)
    response = await client.get(
        "/v1/journal-logs/",
        params={"day": search_date.day, "month": search_date.month},
    )
    result = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(result) == 0
