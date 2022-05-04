import logging

from fastapi import FastAPI

from five_year_journal.api.v1 import v1_router
from five_year_journal.db import init_db

logger = logging.getLogger(__name__)

api = FastAPI()

api.include_router(v1_router)


@api.on_event("startup")
async def on_startup():
    from ..models.accounts import Account  # noqa
    from ..models.journal_logs import JournalLog  # noqa

    logger.info("Initializing database...")
    await init_db()


@api.get("/ping")
def ping():
    return "pong"
