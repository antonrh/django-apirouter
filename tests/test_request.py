from unittest import mock

import pytest
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http import QueryDict
from django.test import RequestFactory

from apirouter.exceptions import APIException
from apirouter.request import Request


@pytest.fixture()
def dummy_request(rf: RequestFactory):
    return Request(rf.get("/"))


def test_request_getattr(rf: RequestFactory):
    request = Request(rf.get("/", data={"a": 1, "b": 2}))

    assert request.GET == QueryDict("a=1&b=2")


def test_request_getattr_missing(dummy_request: Request):
    with pytest.raises(AttributeError) as exc_info:
        getattr(dummy_request, "missing_attribute")

    assert (
        str(exc_info.value) == "'Request' object has no attribute 'missing_attribute'"
    )


def test_request_method(rf: RequestFactory):
    request = Request(rf.post("/"))

    assert request.method == "POST"


def test_request_path(rf: RequestFactory):
    request = Request(rf.get("/path"))

    assert request.path == "/path"
    assert request.path_info == "/path"


def test_request_query_params(rf: RequestFactory):
    request = Request(rf.get("/", data={"a": 1}))

    assert request.query_params == QueryDict("a=1")


def test_request_form(rf: RequestFactory):
    request = Request(rf.post("/", data={"a": 1}))

    assert request.form == QueryDict("a=1")


def test_request_files(rf: RequestFactory):
    request = Request(rf.post("/"))

    assert request.files == {}


def test_request_cookies(dummy_request: Request):
    assert dummy_request.cookies == {}


def test_request_resolver_match(dummy_request: Request):
    assert dummy_request.resolver_match is None


def test_request_content_type(rf: RequestFactory):
    request = Request(rf.post("/", content_type="application/json"))

    assert request.content_type == "application/json"


def test_request_content_params(rf: RequestFactory):
    request = Request(rf.post("/", content_type="application/json;a=1;b=2"))

    assert request.content_params == {"a": "1", "b": "2"}


def test_request_headers(rf: RequestFactory):
    request = Request(rf.get("/", **{"HTTP_X_TEST": "value"}))

    assert request.headers == {"Cookie": "", "X-Test": "value"}


def test_request_schema(dummy_request: Request):
    assert dummy_request.scheme == "http"


def test_request_encoding(dummy_request: Request):
    dummy_request.encoding = "utf-8"

    assert dummy_request.encoding == "utf-8"


def test_request_upload_handlers(dummy_request: Request):
    upload_handler = TemporaryFileUploadHandler()

    dummy_request.upload_handlers = [upload_handler]

    assert dummy_request.upload_handlers == [upload_handler]


@pytest.mark.parametrize(
    "method_name",
    [
        "get_host",
        "get_port",
        "get_full_path",
        "get_full_path_info",
        "get_raw_uri",
        "build_absolute_uri",
        "is_secure",
        "close",
        "read",
        "readline",
        "__iter__",
        "readlines",
    ],
)
def test_request_proxy_methods_no_args(method_name: str):
    request_mock = mock.MagicMock()
    request = Request(request_mock)

    request_method = getattr(request, method_name)
    request_method()

    request_method_mock = getattr(request_mock, method_name)
    request_method_mock.assert_called_once()


@pytest.mark.parametrize(
    "method_name,args,kwargs",
    [
        (
            "get_signed_cookie",
            ["test"],
            {"default": "test", "salt": "", "max_age": None},
        ),
        ("parse_file_upload", [{}, {}], {}),
    ],
)
def test_request_proxy_methods_with_args(method_name: str, args: list, kwargs: dict):
    request_mock = mock.MagicMock()
    request = Request(request_mock)

    request_method = getattr(request, method_name)
    request_method(*args, **kwargs)

    request_method_mock = getattr(request_mock, method_name)
    request_method_mock.assert_called_once_with(*args, **kwargs)


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
