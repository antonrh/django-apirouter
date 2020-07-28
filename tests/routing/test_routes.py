import pytest
from django.http import HttpResponse
from django.views import View

from apirouter import APIRouter

pytestmark = [pytest.mark.urls(__name__)]


router = APIRouter()


@router.route("/")
def route(request):
    return HttpResponse(f"{request.method} /")


@router.route("/method", methods=["GET", "POST"])
def method(request):
    return HttpResponse(f"{request.method} /method")


@router.get("/method/get")
def method_get(request):
    return HttpResponse("GET /get")


@router.put("/method/put")
def method_put(request):
    return HttpResponse("PUT /method/put")


@router.post("/method/post")
def method_post(request):
    return HttpResponse("POST /method/post")


@router.patch("/method/patch")
def method_patch(request):
    return HttpResponse("PATCH /method/patch")


@router.delete("/method/delete")
def method_delete(request):
    return HttpResponse("DELETE /method/delete")


@router.options("/method/options")
def method_options(request):
    return HttpResponse("OPTIONS /method/options")


@router.trace("/method/trace")
def method_trace(request):
    return HttpResponse("TRACE /method/trace")


@router.head("/method/head")
def method_head(request):
    return HttpResponse("HEAD /method/head")


@router.view("/view")
class IndexView(View):
    def get(self, request):
        return HttpResponse("GET /view")

    def post(self, request):
        return HttpResponse("POST /view")


urlpatterns = router.urls


def test_index_get(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.content == b"GET /"


def test_index_post(client):
    response = client.post("/")

    assert response.status_code == 200
    assert response.content == b"POST /"


def test_method_get(client):
    response = client.get("/method")

    assert response.status_code == 200
    assert response.content == b"GET /method"


def test_method_post(client):
    response = client.post("/method")

    assert response.status_code == 200
    assert response.content == b"POST /method"


def test_method_not_allowed(client):
    response = client.delete("/method")

    assert response.status_code == 405
    assert response["Allow"] == "GET, POST"


def test_method_get_route(client):
    response = client.get("/method/get")

    assert response.status_code == 200


def test_view_get(client):
    response = client.get("/view")

    assert response.status_code == 200
    assert response.content == b"GET /view"


def test_view_post(client):
    response = client.post("/view")

    assert response.status_code == 200
    assert response.content == b"POST /view"


def test_view_not_allowed(client):
    response = client.delete("/view")

    assert response.status_code == 405
    assert response["Allow"] == "GET, POST, HEAD, OPTIONS"
