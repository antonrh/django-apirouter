from typing import Any

import pytest
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import RequestFactory

from apirouter import Request
from apirouter.exception_handler import exception_handler
from apirouter.exceptions import APIException


@pytest.mark.parametrize(
    "exc,status_code,content",
    [
        (Http404(), 404, b'{"detail": "Not Found"}'),
        (PermissionDenied(), 403, b'{"detail": "Forbidden"}'),
        (APIException(status_code=400), 400, b'{"detail": "Bad Request"}'),
    ],
)
def test_exception_handler(
    exc: Exception, status_code: int, content: Any, rf: RequestFactory
):
    request = Request(rf.get("/"))
    response = exception_handler(request, exc)

    assert response.status_code == status_code
    assert response.content == content


def test_exception_handler_unhandled(rf: RequestFactory):
    request = Request(rf.get("/"))

    with pytest.raises(Exception) as exc_info:
        exception_handler(request, Exception("unknown error"))

    assert str(exc_info.value) == "unknown error"
