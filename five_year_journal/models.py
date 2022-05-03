from datetime import datetime

from sqlmodel import Field, SQLModel

from .utils import generate_uuid


class BaseModel(SQLModel):
    id: str | None = Field(default_factory=generate_uuid, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(
        None, sa_column_kwargs={"onupdate": datetime.utcnow()}
    )


class JournalLog(BaseModel, table=True):
    content: str
