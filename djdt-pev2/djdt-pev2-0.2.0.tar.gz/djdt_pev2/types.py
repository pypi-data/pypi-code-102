import datetime as dt
import uuid
from typing import Literal, TypedDict


class UnexplainedQuery(TypedDict):
    created: dt.datetime
    sql: str
    duration: float
    db_alias: str
    stacktrace: str
    plan_id: uuid.uuid4
    mode: Literal["explain", "analyze"]
    url: str


class ExplainedQuery(TypedDict):
    created: dt.datetime
    sql: str
    duration: float
    db_alias: str
    stacktrace: str
    plan_id: uuid.uuid4
    mode: Literal["explain", "analyze"]
    # explain or analyze json
    formatted_sql: str
    plan: str
    plan_title: str
