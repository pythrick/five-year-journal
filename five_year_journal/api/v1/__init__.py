from fastapi import APIRouter

from .accounts import accounts_router
from .auth import auth_router
from .journal_logs import journal_logs_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth_router)
v1_router.include_router(journal_logs_router)
v1_router.include_router(accounts_router)
