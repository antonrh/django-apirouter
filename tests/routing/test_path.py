import pytest
from django.views import View

from apirouter.decorators import route, view
from apirouter.request import Request
from apirouter.response import Response
from apirouter.routing import APIRouter

pytestmark = [pytest.mark.urls(__name__)]


class MyRequest(Request):
    @property
    def param(self) -> str:
        return "test"


@route(request_class=MyRequest)
def index(request: MyRequest):
    return Response(f"param - {request.param}")


@view(request_class=MyRequest)
class IndexView(View):
    def get(self, request: MyRequest):
        return Response(f"param - {request.param}")


router = APIRouter()

urlpatterns = [router.path("func/", index), router.path("view/", IndexView.as_view())]


def test_router_path_func_view(client):
    response = client.get("/func/")

    assert response.status_code == 200
    assert response.content == b"param - test"


def test_router_path_class_view(client):
    response = client.get("/view/")

    assert response.status_code == 200
    assert response.content == b"param - test"
