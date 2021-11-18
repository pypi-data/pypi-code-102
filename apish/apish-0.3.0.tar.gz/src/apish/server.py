import os

import uvicorn
from starlette.applications import Starlette


SERVER_PORT = "8080"


def run(app: Starlette, **kwargs):
    # The log_config argument takes a logging.dictConfig that is applied to the
    # uvicorn logging.
    uvicorn.run(app, port=int(os.environ.get("SERVER_PORT", SERVER_PORT)), **kwargs)
