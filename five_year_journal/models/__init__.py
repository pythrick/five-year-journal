import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Column
from sqlmodel import Field, SQLModel

from five_year_journal.types import UUIDType


class BaseModel(SQLModel):
    id: UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUIDType(), primary_key=True, unique=True),
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(
        None, sa_column_kwargs={"onupdate": datetime.utcnow()}
    )
