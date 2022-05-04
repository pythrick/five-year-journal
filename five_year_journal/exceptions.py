from dataclasses import dataclass, field
from typing import Any

from fastapi import HTTPException, status


@dataclass
class ExceptionWithValues(Exception):
    message: str
    values: dict = field(default_factory=dict)


class InvalidCredentials(ExceptionWithValues):
    pass


@dataclass
class BaseHttpException(HTTPException):
    detail: Any = None
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    headers: dict[str, Any] | None = None


@dataclass
class ModelNotFound(BaseHttpException):
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class Unauthorized(BaseHttpException):
    status_code: int = status.HTTP_401_UNAUTHORIZED


@dataclass
class Forbidden(BaseHttpException):
    status_code: int = status.HTTP_403_FORBIDDEN


@dataclass
class Conflict(BaseHttpException):
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class InvalidEmail(BaseHttpException):
    detail: str = "Invalid email."


class InvalidToken(Forbidden):
    pass
