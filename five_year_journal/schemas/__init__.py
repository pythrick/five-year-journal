from pydantic import BaseModel

from ..helpers import to_camel


class BaseSchema(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
