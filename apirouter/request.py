import json
from http import HTTPStatus
from typing import Any, Optional

from django.http import HttpRequest
from django.http.request import HttpHeaders
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from apirouter.exceptions import APIException

_missing = object()


class Request:
    def __init__(self, request: HttpRequest):
        self._request = request
        self._json: Optional[Any] = _missing

    def __getattr__(self, attr: str) -> Any:
        try:
            return getattr(self._request, attr)
        except AttributeError:
            return self.__getattribute__(attr)

    @property
    def method(self) -> str:
        return self._request.method

    @property
    def path(self) -> str:
        return self._request.path

    @cached_property
    def headers(self) -> HttpHeaders:
        return self._request.headers

    @property
    def body(self) -> bytes:
        return self._request.body

    def json(self) -> Any:
        if self._json is _missing:
            try:
                self._json = json.loads(self.body)
            except ValueError:
                raise APIException(
                    status_code=HTTPStatus.BAD_REQUEST, detail=_("Invalid JSON body.")
                )
        return self._json
