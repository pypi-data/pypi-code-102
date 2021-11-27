class Request:
    def __init__(self, url, method="GET", payload=None, headers=None):
        self.method = method
        self.url = url
        self.payload = payload
        self.headers = headers if headers is not None else {}

    def merge_headers(self, new_headers):
        self.headers.update(new_headers)
