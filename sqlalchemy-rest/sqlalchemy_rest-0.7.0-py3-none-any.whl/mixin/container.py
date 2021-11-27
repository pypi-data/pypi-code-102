from typing import Dict, NamedTuple, Optional, Sequence, Union

__all__ = [
    'PagerParams',
    'SearchParams',
]


class PagerParams(NamedTuple):
    page: int
    start: int
    limit: int
    asc: Sequence[bool]
    sort_by: Sequence[str]


class SearchParams(NamedTuple):
    search: Dict[str, str] = {}
    and_joint: Optional[bool] = None
    search_type: Dict[str, Union[int, Dict[str, int]]] = {}
