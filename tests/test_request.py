import pytest

from apirouter.exceptions import APIException
from apirouter.request import Request


def test_request_json(rf):
    request = Request(rf.post("/", data="{}", content_type="application/json"))

    assert request.json() == {}


def test_request_json_invalid(rf):
    request = Request(rf.post("/", data="{", content_type="application/json"))

    with pytest.raises(APIException) as exc_info:
        request.json()

    exc = exc_info.value

    assert exc.status_code == 400
    assert exc.detail == "Invalid JSON body."
