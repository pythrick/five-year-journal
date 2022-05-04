from . import BaseSchema


class AuthIn(BaseSchema):
    email: str
    password: str


class AuthInResponse(BaseSchema):
    access_token: str
    refresh_token: str


class RefreshIn(BaseSchema):
    refresh_token: str


class RefreshInResponse(AuthInResponse):
    ...
