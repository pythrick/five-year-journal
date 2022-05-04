from typing import List

from pydantic import validator
from sqlalchemy import UniqueConstraint
from sqlmodel import Relationship

from ..helpers import get_password_hash
from . import BaseModel


class Account(BaseModel, table=True):
    __table_args__ = (UniqueConstraint("email"),)
    __tablename__ = "accounts"

    name: str
    email: str
    password: str
    is_active: bool = True
    is_verified: bool = False

    journal_logs: List["JournalLog"] = Relationship(  # noqa:F821
        back_populates="account"
    )

    @validator("password")
    def hash_password(cls, v):
        return get_password_hash(v)
