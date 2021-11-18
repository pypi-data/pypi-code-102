import datetime
import json
import traceback
import uuid
from contextlib import contextmanager
from typing import Literal, Optional

import sqlparse
from django.conf import settings
from django.core.cache import cache
from django.db import connection, connections, reset_queries
from django.http.response import Http404
from django.urls import reverse

from djdt_pev2.types import ExplainedQuery, UnexplainedQuery

EXPLAIN_TEMPLATE = "EXPLAIN (COSTS, VERBOSE, FORMAT JSON) {}"
ANALYZE_TEMPLATE = "EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON) {}"
UNEXPLAINED_QUERY_KEY_TEMPLATE = "SQL_UNEXPLAINED_QUERY:{plan_id}"
EXPLAINED_QUERY_KEY_TEMPLATE = "SQL_EXPLAINED_QUERY:{plan_id}"


@contextmanager
def explain_queries(
    db_alias: Optional[str] = None,
    analyze: bool = False,
    trace_limit: int = 10,
    sql_length: int = 100,
    timeout: int = 300,
):
    """Context manager to provide links to explained queries.
    :param db_alias: Which
    :param analyze:
    :param trace_limit:
    :param sql_length:
    :param timeout: Store unexplained queries for `timeout` seconds. Defaults to 5 minutes.

    usage:
    with explain_queries(analyze=True):
        # This query will be captured and a link to an explain displayed
        User.objects.count()
    """
    reset_queries()
    yield
    if db_alias is None:
        queries_after = connection.queries[:]
    else:
        queries_after = connection[db_alias].queries[:]
    for i, q in enumerate(queries_after):
        query_time = q["time"]
        query_sql = q["sql"]
        stacktrace = "".join(traceback.format_stack()[-trace_limit:-2])
        r = store_unexplained_query(
            sql=query_sql,
            db_alias=db_alias or "default",
            duration=query_time,
            mode="analyze" if analyze else "explain",
            stacktrace=stacktrace,
            timeout=timeout,
        )
        print(f"\u001b[31m[{i}]\u001b[0m \u001b[32m{r['url']}\u001b[0m \n {query_sql[:sql_length]}")


def get_explained_plan(plan_id: str) -> ExplainedQuery:
    """Fetches cached plan otherwise gets unexplained query and generates a result"""
    if explained_query := cache.get(key=EXPLAINED_QUERY_KEY_TEMPLATE.format(plan_id=plan_id)):
        return explained_query
    if unexplained_query := cache.get(key=UNEXPLAINED_QUERY_KEY_TEMPLATE.format(plan_id=plan_id)):
        db_alias = unexplained_query["db_alias"]
        with connections[db_alias].cursor() as cursor:
            sql = unexplained_query["sql"]
            sql_template = (
                EXPLAIN_TEMPLATE if unexplained_query["mode"] == "explain" else ANALYZE_TEMPLATE
            )
            cursor.execute("set statement_timeout TO 8000;")
            cursor.execute(sql_template.format(sql))
            result = cursor.fetchall()
            plan = result[0][0]

        explained_query = ExplainedQuery(
            **unexplained_query,
            plan=json.dumps(plan),
            plan_title=f"Untitled plan: {plan_id}",
            formatted_sql=sqlparse.format(
                unexplained_query["sql"], reindent=True, keyword_case="upper"
            ),
        )

        cache.set(
            EXPLAINED_QUERY_KEY_TEMPLATE.format(plan_id=plan_id),
            explained_query,
            timeout=getattr(settings, "PEV2_SQL_ANALYZE_TIMEOUT", 24 * 60 * 60),
        )

        return explained_query
    else:
        raise Http404(f"Could not find plan_id: {plan_id}")


def store_unexplained_query(
    sql: str,
    duration: float,
    db_alias: str,
    mode: Literal["explain", "analyze"],
    stacktrace: str = "",
    timeout: Optional[int] = None,
) -> UnexplainedQuery:
    plan_id = str(uuid.uuid4())
    created = datetime.datetime.now()
    unexplained_query = UnexplainedQuery(
        created=created,
        sql=sql,
        duration=duration,
        db_alias=db_alias,
        stacktrace=stacktrace,
        plan_id=plan_id,
        mode=mode,
        url=reverse("djdt:pev2_visualize", args=(plan_id,)),
    )
    cache.set(
        UNEXPLAINED_QUERY_KEY_TEMPLATE.format(plan_id=plan_id),
        unexplained_query,
        timeout=timeout or getattr(settings, "PEV2_SQL_ANALYZE_TIMEOUT", 24 * 60 * 60),
    )
    return unexplained_query
