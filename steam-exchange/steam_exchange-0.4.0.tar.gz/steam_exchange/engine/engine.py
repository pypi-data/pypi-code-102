import requests

from .browser import HEADERS
from .session import Session


class Engine:
    def __init__(self, session: Session, browser_headers=None):
        self._browser_headers = (
            browser_headers if browser_headers is not None else HEADERS
        )
        self._session = session

    def request(self, r):
        req = r.build_request(self._session)
        headers = req.headers
        headers.update(self._browser_headers)
        headers["Cookie"] = self._session.build_cookie()
        resp = requests.request(
            req.method, req.url, data=req.payload, headers=headers
        )
        if not resp.ok:
            print(req.url)
            print(resp)
            print(resp.text)
        return r.response(resp)
