import pytest
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from apirouter import APIRouter

pytestmark = [pytest.mark.urls(__name__)]


class TestMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response["x-middleware-test"] = "yes"
        return response


router = APIRouter(middleware_classes=[TestMiddleware])


@router.get("/middleware")
def middleware_get(request):
    return HttpResponse("GET /middleware")


urlpatterns = router.urls


def test_middleware_get(client):
    response = client.get("/middleware")

    assert response.status_code == 200
    assert response.content == b"GET /middleware"
    assert response["x-middleware-test"] == "yes"
