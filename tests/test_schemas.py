from typing import Any, Callable, Coroutine

import pytest
from pydantic import ValidationError

from five_year_journal.models.journal_logs import JournalLog
from five_year_journal.schemas.journal_logs import (
    JournalLogIn,
    JournalLogInResponse,
)


def test_job_log_in_schema():
    data = {"content": "xxxx"}
    result = JournalLogIn(**data)
    assert result == JournalLogIn(content="xxxx")


def test_job_log_in_schema_missing_required_field():
    data = {}
    with pytest.raises(ValidationError) as exc:
        JournalLogIn(**data)
    assert str(exc.value) == (
        "1 validation error for JournalLogIn\n"
        "content\n"
        "  field required (type=value_error.missing)"
    )


async def test_job_log_out_schema(
    journal_logs_factory: Callable[
        [int], Coroutine[Any, Any, list[JournalLog]]
    ]
):
    journal_log = (await journal_logs_factory(1))[0]
    result = JournalLogInResponse.from_orm(journal_log)
    assert result == JournalLogInResponse(
        id=journal_log.id,
        content=journal_log.content,
        created_at=journal_log.created_at,
        updated_at=journal_log.updated_at,
    )
