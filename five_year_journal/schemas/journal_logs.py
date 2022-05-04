from datetime import datetime
from typing import Optional
from uuid import UUID

from . import BaseSchema


class JournalLogIn(BaseSchema):
    content: str


class JournalLogInResponse(JournalLogIn):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
