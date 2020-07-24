from typing import Any

from django.http import HttpRequest


class Request:
    def __init__(self, request: HttpRequest):
        self._request = request

    def __getattr__(self, attr: str) -> Any:
        try:
            return getattr(self._request, attr)
        except AttributeError:
            return self.__getattribute__(attr)

    @property
    def method(self) -> str:
        return self._request.method
