from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .utils import to_camel


class BaseSchema(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class JournalLogIn(BaseSchema):
    content: str


class JournalLogOut(JournalLogIn):
    id: UUID
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True
