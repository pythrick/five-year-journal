import logging
from datetime import datetime

from fastapi import Depends, FastAPI, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from five_year_journal.core import create_journal_log, list_journal_logs
from five_year_journal.db import init_db
from five_year_journal.dependencies import get_session
from five_year_journal.schemas import JournalLogIn, JournalLogOut

logger = logging.getLogger(__name__)

api = FastAPI()


@api.on_event("startup")
async def on_startup():
    from .models import JournalLog  # noqa

    logger.info("Initializing database...")
    await init_db()


@api.get("/ping")
def ping():
    return "pong"


@api.post(
    "/v1/journal-logs/",
    response_model=JournalLogOut,
    status_code=status.HTTP_201_CREATED,
)
async def new_journal_log(
    journal_log: JournalLogIn, session: AsyncSession = Depends(get_session)
):
    response = await create_journal_log(session, journal_log)
    return response


@api.get("/v1/journal-logs/", response_model=list[JournalLogOut])
async def list_journal_logs_from_past_years(
    day: int | None = Query(None),
    month: int | None = Query(None),
    limit: int = Query(5),
    offset: int = Query(1),
    session: AsyncSession = Depends(get_session),
):
    day = day or datetime.utcnow().day
    month = month or datetime.utcnow().month
    response = await list_journal_logs(session, day, month, limit, offset)
    return response
