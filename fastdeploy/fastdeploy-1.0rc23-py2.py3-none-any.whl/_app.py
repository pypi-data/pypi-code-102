from gevent import monkey

monkey.patch_all()
import gevent
import gevent.pool
import os
import sys
import glob
import time
import uuid
import ujson
import falcon
import base64
import shutil
import datetime
import logging
import epyk
from functools import partial

from . import _utils

while "META.time_per_example" not in _utils.LOG_INDEX:
    _utils.logger.info(f"Waiting for batch size search to finish.")
    time.sleep(5)

ONLY_ASYNC = os.getenv("ONLY_ASYNC", False)

TIME_PER_EXAMPLE = _utils.LOG_INDEX["META.time_per_example"]


def wait_and_read_pred(unique_id):
    """
    Waits for and reads result for unique_id.

    :param unique_id: unique_id of the input

    :return response: json dumped python dict with keys "success" and "prediction"/ "reason"
    :return status: HTTP status code
    """
    # Keeping track of start_time for TIMEOUT implementation
    start_time = time.time()
    # Default response and status
    response, status = (
        {"success": False, "reason": "timeout"},
        falcon.HTTP_503,
    )
    while True:
        try:
            # if result doesn't exist for this uuid,  while loop continues/
            pred, metrics = _utils.RESULTS_INDEX[unique_id]
            try:
                response = {"prediction": pred, "success": True}
            # if return dict has any non json serializable values, we str() it
            except:
                _utils.logger.info(
                    f"unique_id: {unique_id} could not json serialize the result."
                )
                response = {"prediction": str(pred), "success": True}
            status = falcon.HTTP_200
            break
        except:
            # stop in case of timeout
            if time.time() - start_time >= _utils.TIMEOUT:
                _utils.logger.warn(
                    f"unique_id: {unique_id} timedout, with timeout {_utils.TIMEOUT}"
                )
                break

            gevent.time.sleep(TIME_PER_EXAMPLE * 0.501)
            metrics = {}

    return response, status, metrics


class Infer(object):
    def on_post(self, req, resp):
        try:
            unique_id = str(uuid.uuid4())
            metrics = {
                "received": time.time(),
                "prediction_start": -1,
                "prediction_end": -1,
                "batch_size": len(req.media["data"]),
                "predicted_in_batch": -1,
                "responded": -1,
            }
            _utils.REQUEST_QUEUE.appendleft((unique_id, req.media["data"], metrics))

            if ONLY_ASYNC:
                resp.media = {"unique_id": unique_id}
                resp.status = falcon.HTTP_200
            else:
                preds, status, _metrics = wait_and_read_pred(unique_id)

                if not len(_metrics):
                    _metrics = metrics

                _metrics["responded"] = time.time()
                _utils.LOG_INDEX[unique_id] = (_metrics, req.media["data"])

                resp.media = preds
                resp.status = status

        except Exception as ex:
            _utils.logger.exception(ex, exc_info=True)
            resp.media = {"success": False, "reason": str(ex)}
            resp.status = falcon.HTTP_400


class Metrics(object):
    def on_get(self, req, resp):

        try:
            end_time = int(req.params.get("from_time", time.time()))
            total_time = int(req.params.get("total_time", 600))

            loop_batch_size = _utils.LOG_INDEX["META.batch_size"]
            batch_size_to_time_per_example = _utils.LOG_INDEX[
                "META.batch_size_to_time_per_example"
            ]

            first_end_time = 0
            all_results_in_time_period = []

            current_time = time.time()

            for _ in reversed(_utils.LOG_INDEX):
                if _[:5] == "META.":
                    continue

                (metrics, in_data), result = (
                    _utils.LOG_INDEX[_],
                    _utils.RESULTS_INDEX[_],
                )

                if metrics["received"] <= end_time:
                    all_results_in_time_period.append(
                        {
                            "unique_id": _,
                            "loop_time_per_example": loop_time_per_example,
                            "received_on": metrics["received"] - current_time,
                            "prediction_time_per_example": (
                                metrics["prediction_end"] - metrics["prediction_start"]
                            )
                            / metrics["predicted_in_batch"],
                            "latency": metrics["prediction_start"]
                            - metrics["received"]
                            + metrics["responded"]
                            - metrics["prediction_end"],
                        }
                    )
                    if first_end_time == 0:
                        first_end_time = metrics["received"]

                if metrics["received"] + total_time < end_time:
                    break

            page = epyk.Page()
            page.headers.dev()
            js_data = page.data.js.record(data=all_results_in_time_period)

            line = page.ui.charts.chartJs.line(
                all_results_in_time_period,
                y_columns=["prediction_time_per_example", "loop_time_per_example"],
                x_axis="unique_id",
            )
            page.ui.row([line])

            print(dir(page.outs))

            resp.text = page.outs.html()
            resp.content_type = "text/html"
            resp.status = falcon.HTTP_200
        except Exception as ex:
            logging.exception(ex, exc_info=True)
            pass


class Res(object):
    def on_post(self, req, resp):
        try:
            unique_id = req.media["unique_id"]
            _utils.logger.info(f"unique_id: {unique_id} Result request received.")
            resp.media = {"success": None, "reason": "processing"}
            resp.status = falcon.HTTP_200

        except Exception as ex:
            _utils.logger.exception(ex, exc_info=True)
            resp.media = {"success": False, "reason": str(ex)}
            resp.status = falcon.HTTP_400


json_handler = falcon.media.JSONHandler(
    loads=ujson.loads, dumps=partial(ujson.dumps, ensure_ascii=False)
)

extra_handlers = {
    "application/json": json_handler,
}

app = falcon.App(cors_enable=True)
app.req_options.media_handlers.update(extra_handlers)
app.resp_options.media_handlers.update(extra_handlers)
app.req_options.auto_parse_form_urlencoded = True
app = falcon.App(
    middleware=falcon.CORSMiddleware(
        allow_origins=_utils.ALLOWED_ORIGINS, allow_credentials=_utils.ALLOWED_ORIGINS
    )
)

infer_api = Infer()
res_api = Res()
metrics_api = Metrics()
app.add_route("/infer", infer_api)

# Backwards compatibility
app.add_route("/sync", infer_api)
app.add_route("/result", res_api)
app.add_route("/metrics", metrics_api)

if __name__ == "__main__":
    batch_size = _utils.RESULTS_INDEX["META.batch_size"]

    from gunicorn.app.wsgiapp import WSGIApplication

    WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]").run()

    from gevent import pywsgi

    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")

    print(f"fastDeploy active at http://{host}:{port}")

    server = pywsgi.WSGIServer((host, port), app, spawn=1000, log=None)
    server.serve_forever()
