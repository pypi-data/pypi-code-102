from typing import Any

from starlette.requests import Request

from .base_filter import get_filters
from ..schemas.term_and_condition import TermAndConditionIn, TermAndConditionFilter
from ..models.term_and_condition import TermAndCondition


def get_term_and_condition_filters(*, request: Request) -> Any:
    data = dict(
        is_active=TermAndCondition.is_active,
        is_archive=TermAndCondition.is_archive,
        created_at__gt=TermAndCondition.created_at,
        created_at__lt=TermAndCondition.created_at,
        created_at=TermAndCondition.created_at,
    )
    return get_filters(request, TermAndConditionFilter, data)
