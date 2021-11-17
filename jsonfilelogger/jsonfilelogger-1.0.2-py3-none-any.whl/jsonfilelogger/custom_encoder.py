from typing import Any
import datetime
import json


class CustomEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime.datetime):
            return str(o)
        else:
            return super().default(o)
