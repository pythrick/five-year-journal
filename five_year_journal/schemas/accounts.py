from uuid import UUID

from . import BaseSchema


class AccountIn(BaseSchema):
    name: str
    email: str
    password: str


class AccountInResponse(BaseSchema):
    id: UUID
    name: str
    email: str

    class Config:
        orm_mode = True
