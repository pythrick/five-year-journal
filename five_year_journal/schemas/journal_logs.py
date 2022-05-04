from datetime import datetime
from uuid import UUID

from . import BaseSchema


class JournalLogIn(BaseSchema):
    content: str


class JournalLogInResponse(JournalLogIn):
    id: UUID
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True
