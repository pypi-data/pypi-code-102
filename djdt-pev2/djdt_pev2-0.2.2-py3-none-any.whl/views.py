from logging import getLogger

from debug_toolbar.decorators import require_show_toolbar, signed_data_view
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
from django.template.response import SimpleTemplateResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt

from djdt_pev2.forms import Pev2SQLSelectForm

from .utils import get_explained_plan, store_unexplained_query

logger = getLogger("djdt_pev2")


@require_show_toolbar
@xframe_options_sameorigin
def pev2_explain_iframe(request, plan_id):
    if not plan_id:
        return HttpResponseBadRequest("Missing result UUID ")

    context = get_explained_plan(plan_id)

    return SimpleTemplateResponse("djdt_pev2/panels/pev_iframe.html", context=context)


def process_view(request, verified_data, mode):
    """Returns the output of the SQL EXPLAIN on the given query"""
    form = Pev2SQLSelectForm(verified_data)

    if form.is_valid():
        sql = form.cleaned_data["sql"]
        vendor = form.connection.vendor
        if vendor != "postgresql":
            raise NotImplementedError("Only postgresql is supported")

        unexplained_query = store_unexplained_query(
            sql=sql,
            duration=form.cleaned_data["duration"],
            db_alias=form.cleaned_data["alias"],
            stacktrace=form.cleaned_data["stacktrace"],
            mode=mode,
        )

        context = {"request": request, "url": unexplained_query["url"]}

        content = render_to_string("djdt_pev2/panels/sql_explain.html", context)
        return JsonResponse({"content": content})
    return HttpResponseBadRequest("Form errors")


@csrf_exempt
@require_show_toolbar
@signed_data_view
def sql_analyze(request, verified_data):
    return process_view(request, verified_data, mode="explain")


@csrf_exempt
@require_show_toolbar
@signed_data_view
def sql_explain(request, verified_data):
    return process_view(request, verified_data, mode="analyze")
