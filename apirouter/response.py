from typing import Any, Optional

from django.http.request import HttpHeaders
from django.http.response import JsonResponse as DjangoJsonResponse


class JsonResponse(DjangoJsonResponse):
    def __init__(self, data: Any, headers: Optional[HttpHeaders] = None, **kwargs):
        kwargs["safe"] = False
        super().__init__(data, **kwargs)

        if headers:
            for name, value in headers.items():
                self[name] = value
