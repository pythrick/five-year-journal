from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from five_year_journal.config import settings

engine = create_async_engine(
    settings.database_dsn.get_secret_value(), echo=settings.debug, future=True
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
