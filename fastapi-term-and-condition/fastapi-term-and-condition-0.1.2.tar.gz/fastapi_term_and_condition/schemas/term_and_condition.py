from datetime import datetime
from typing import Optional

from .base import BaseSchema


class TermAndConditionIn(BaseSchema):
    key: str
    value: str
    category: Optional[str]
    additional_data: Optional[dict]
    is_active: Optional[bool]
    is_archive: Optional[bool]


class TermAndConditionFilter(BaseSchema):
    is_active: Optional[bool]
    is_archive: Optional[bool]
    id: Optional[int]
    updated_at: Optional[datetime]
    created_at: Optional[datetime]


class TermAndConditionOut(TermAndConditionIn):
    id: int
    updated_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
