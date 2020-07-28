import pytest
from django.http import QueryDict

from apirouter.exceptions import APIException
from apirouter.request import Request


def test_request_getattr(rf):
    request = Request(rf.get("/", data={"a": 1, "b": 2}))

    assert request.GET == QueryDict("a=1&b=2")


def test_request_method(rf):
    request = Request(rf.post("/"))

    assert request.method == "POST"


def test_request_get_path(rf):
    request = Request(rf.get("/path"))

    assert request.path == "/path"
    assert request.path_info == "/path"


def test_request_query_params(rf):
    request = Request(rf.get("/", data={"a": 1}))

    assert request.query_params == QueryDict("a=1")


def test_request_resolver_match(rf):
    request = Request(rf.get("/"))

    assert request.resolver_match is None


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
