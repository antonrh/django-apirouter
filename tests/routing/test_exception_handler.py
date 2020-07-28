import pytest

from apirouter.exception_handler import exception_handler
from apirouter.exceptions import APIException
from apirouter.request import Request


def test_exception_handler_api_exception(rf):
    request = Request(rf.get("/"))

    response = exception_handler(
        request, APIException(status_code=400, detail="Error", headers={"x-test": "1"})
    )

    assert response.status_code == 400
    assert response.content == b'{"detail": "Error"}'
    assert response.has_header("x-test")


def test_exception_handler_not_handler(rf):
    request = Request(rf.get("/"))

    with pytest.raises(Exception) as exc_info:
        exception_handler(request, Exception("Unknown error"))

    assert str(exc_info.value) == "Unknown error"
