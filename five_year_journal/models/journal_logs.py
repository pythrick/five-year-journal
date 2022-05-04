from uuid import UUID

from sqlalchemy import Column
from sqlmodel import Field, Relationship

from ..types import UUIDType
from . import BaseModel
from .accounts import Account


class JournalLog(BaseModel, table=True):
    __tablename__ = "journal_logs"

    content: str
    account_id: UUID = Field(
        foreign_key="accounts.id", sa_column=Column(UUIDType())
    )
    account: Account = Relationship(back_populates="journal_logs")
