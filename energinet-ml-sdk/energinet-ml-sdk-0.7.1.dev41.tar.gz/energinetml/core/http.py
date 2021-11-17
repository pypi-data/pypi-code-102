#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[summary]
"""

import logging
import traceback
from typing import TYPE_CHECKING, Callable  # noqa TYP001

import fastapi
import uvicorn
from opentelemetry import trace
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

from energinetml.core.predicting import PredictionController, PredictResponse
from energinetml.settings import APPINSIGHTS_INSTRUMENTATIONKEY, PACKAGE_REQUIREMENT

if TYPE_CHECKING:
    from energinetml.core.model import Model, TrainedModel

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


def create_app(
    model: "Model", trained_model: "TrainedModel", model_version: str = None
) -> fastapi.FastAPI:
    """[summary]

    Args:
        model (Model): [description]
        trained_model (TrainedModel): [description]
        model_version (str, optional): [description]. Defaults to None.

    Returns:
        fastapi.FastAPI: [description]
    """
    controller = PredictionController(
        model=model, trained_model=trained_model, model_version=model_version
    )

    async def opentelemetry_middleware(
        request: fastapi.Request, call_next: Callable
    ) -> fastapi.Response:
        """
        FastAPI middleware to record HTTP requests.

        Can not access request body in middleware (for logging):
        Issue description: https://github.com/tiangolo/fastapi/issues/394
        """

        # TODO: Why imports here?
        from opentelemetry.trace import SpanKind, Status
        from opentelemetry.trace.status import StatusCode

        start_span = tracer.start_span(name="request", kind=SpanKind.SERVER)

        with start_span as span:
            span.set_attribute("http.url", str(request.url))
            span.set_attribute("http_url", str(request.url))
            span.set_attribute("model_name", model.name)
            if model_version is not None:
                span.set_attribute("model_version", model_version)

            try:
                response = await call_next(request)
            except Exception as e:
                logger.exception("Prediction failed")
                span.record_exception(e)
                span.set_status(Status(status_code=StatusCode.ERROR))
                span.set_attribute("http.status_code", 500)
                span.set_attribute("http_status_code", 500)
                span.set_attribute("error.name", e.__class__.__name__)
                span.set_attribute("error.message", str(e))
                span.set_attribute("error.stacktrace", traceback.format_exc())
                return fastapi.Response(status_code=500)
            else:
                span.set_status(Status(status_code=StatusCode.OK))
                span.set_attribute("http.status_code", response.status_code)
                span.set_attribute("http_status_code", response.status_code)
                return response

    async def root_http_endpoint() -> RedirectResponse:
        """
        / should redirect to /docs
        """
        return RedirectResponse(url="/docs")

    async def predict_http_endpoint(
        request: controller.request_model, response: fastapi.Response
    ) -> PredictResponse:
        """
        Model prediction HTTP endpoint.
        """
        response.headers["X-sdk-version"] = str(PACKAGE_REQUIREMENT)

        return controller.predict(request)

    async def health_http_endpoint(response: fastapi.Response) -> fastapi.Response:
        """
        Health endpoint, should return status 200 with no specific body.
        """
        response.status_code = 200
        return response

    # -- Setup app -----------------------------------------------------------

    app = fastapi.FastAPI(
        title=model.name,
        description=(f"Model version: {model_version if model_version else None}"),
    )

    if APPINSIGHTS_INSTRUMENTATIONKEY:
        app.add_middleware(
            middleware_class=BaseHTTPMiddleware, dispatch=opentelemetry_middleware
        )

    app.router.add_api_route(path="/", methods=["GET"], endpoint=root_http_endpoint)

    app.router.add_api_route(
        path="/predict",
        methods=["POST"],
        endpoint=predict_http_endpoint,
        response_model=controller.response_model,
        tags=["model"],
        summary="Predict using the model",
    )

    app.router.add_api_route(
        path="/health",
        methods=["GET"],
        endpoint=health_http_endpoint,
        tags=["health"],
        summary="Health endpoint",
        description="Health endpoint, returns status 200",
    )

    return app


def run_predict_api(
    model: "Model",
    trained_model: "TrainedModel",
    host: str,
    port: int,
    model_version: str = None,
) -> None:
    """[summary]

    Args:
        model (Model): [description]
        trained_model (TrainedModel): [description]
        host (str): [description]
        port (int): [description]
        model_version (str, optional): [description]. Defaults to None.
    """
    app = create_app(
        model=model, trained_model=trained_model, model_version=model_version
    )

    uvicorn.run(app=app, host=host, port=port)
