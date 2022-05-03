from datetime import datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from five_year_journal.models import JournalLog
from five_year_journal.schemas import JournalLogIn, JournalLogOut


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


def test_job_log_out_schema():
    current_time = datetime.utcnow()
    data = JournalLog(
        content="xxxx", created_at=current_time, updated_at=current_time
    )
    result = JournalLogOut.from_orm(data)
    assert result == JournalLogOut(
        id=UUID(data.id),
        content="xxxx",
        created_at=current_time,
        updated_at=current_time,
    )
