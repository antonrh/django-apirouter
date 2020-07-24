import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    "viewname,args,kwargs,expected",
    [
        ("root:index", [], {}, "/"),
        ("root:method", [], {}, "/method"),
        ("root:method_get", [], {}, "/method/get"),
        ("root:method_put", [], {}, "/method/put"),
        ("root:method_post", [], {}, "/method/post"),
        ("root:method_patch", [], {}, "/method/patch"),
        ("root:method_delete", [], {}, "/method/delete"),
        ("root:method_options", [], {}, "/method/options"),
        ("root:method_trace", [], {}, "/method/trace"),
        ("root:method_head", [], {}, "/method/head"),
        ("root:view", [], {}, "/view"),
        ("root:middleware:middleware_get", [], {}, "/middleware/get"),
    ],
)
def test_reverse_name(viewname: str, args: list, kwargs: dict, expected: str):
    assert reverse(viewname, args=args, kwargs=kwargs) == expected


def test_root_index_get(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.content == b"GET /"


def test_root_index_post(client):
    response = client.post("/")

    assert response.status_code == 200
    assert response.content == b"POST /"


def test_root_method_get(client):
    response = client.get("/method")

    assert response.status_code == 200
    assert response.content == b"GET /method"


def test_root_method_post(client):
    response = client.post("/method")

    assert response.status_code == 200
    assert response.content == b"POST /method"


def test_root_method_not_allowed(client):
    response = client.delete("/method")

    assert response.status_code == 405
    assert response["Allow"] == "GET, POST"


def test_root_view_get(client):
    response = client.get("/view")

    assert response.status_code == 200
    assert response.content == b"GET /view"


def test_root_view_post(client):
    response = client.post("/view")

    assert response.status_code == 200
    assert response.content == b"POST /view"


def test_root_view_not_allowed(client):
    response = client.delete("/view")

    assert response.status_code == 405
    assert response["Allow"] == "GET, POST, HEAD, OPTIONS"


def test_include_get(client):
    response = client.get("/include/get")

    assert response.status_code == 200
    assert response.content == b"GET /include/get"


def test_middleware_get(client):
    response = client.get("/middleware/get")

    assert response.status_code == 200
    assert response.content == b"GET /middleware/get"
    assert response["x-middleware-test"] == "yes"
