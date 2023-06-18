"""
Модель пользователя
"""
from pydantic import BaseModel, validator

from firezone_api.models.string_datetime_view import StringDatetime


class User(BaseModel):
    id: str
    email: str
    role: str
    updated_at: StringDatetime | None
    disabled_at: StringDatetime | None
    inserted_at: StringDatetime | None
    last_signed_in_at: StringDatetime | None

    class Config:
        arbitrary_types_allowed = True

    @validator("updated_at", "disabled_at",
               "inserted_at", "last_signed_in_at",
               pre=True)
    def parse_date(value: str | None) -> StringDatetime | None:
        if value is None:
            return
        value = value.split('.')[0]
        return StringDatetime(value)
