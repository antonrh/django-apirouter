import http
from typing import Any, Optional


class APIException(Exception):
    def __init__(
        self, status_code: int, detail: Any = None, headers: Optional[dict] = None
    ):
        if detail is None:
            detail = http.HTTPStatus.__call__(status_code).phrase
        self.status_code = status_code
        self.detail = detail
        self.headers = headers

    def __str__(self):
        return self.detail
