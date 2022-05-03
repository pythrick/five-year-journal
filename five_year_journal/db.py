from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from config import settings

engine = create_async_engine(
    settings.database_dsn, echo=settings.debug, future=True
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
