import http
from typing import Any, Optional

from django.http.request import HttpHeaders


class APIException(Exception):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[HttpHeaders] = None,
    ):
        if detail is None:
            detail = http.HTTPStatus.__call__(status_code).phrase
        self.status_code = status_code
        self.detail = detail
        self.headers = headers
