from datetime import datetime
from uuid import UUID

from httpx import AsyncClient


async def test_new_journal_log_v1(client: AsyncClient):
    response = await client.post(
        "/v1/journal-logs/", json={"content": "yyyyy"}
    )
    result = response.json()

    assert response.status_code == 201
    assert len(result["id"]) == 36
    assert UUID(result["id"])
    assert result["content"] == "yyyyy"
    assert result["updatedAt"] is None
    assert (
        datetime.utcnow() - datetime.fromisoformat(result["createdAt"])
    ).total_seconds() < 1
