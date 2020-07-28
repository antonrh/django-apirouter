from typing import Callable, List

import pytest
from django.http import HttpResponse
from django.views import View

from apirouter import APIRouter

pytestmark = [pytest.mark.urls(__name__)]


def append_response_after(response: HttpResponse, item: str) -> str:
    response.setdefault("x-after", "")
    items: List[str] = response["x-after"].split()
    items.append(item)
    items_str = " ".join(items)
    response["x-after"] = items_str
    return items_str


def make_decorator(key: str):
    def decorator(view_func: Callable):
        def wrapped(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            append_response_after(response, key)
            return response

        return wrapped

    return decorator


router = APIRouter(decorators=[make_decorator("router1"), make_decorator("router2")])


@router.get("/func")
@make_decorator("func1")
@make_decorator("func2")
def func_get(request):
    return HttpResponse("GET /func")


@router.view("/view", decorators=[make_decorator("view1"), make_decorator("view2")])
class RouteView(View):
    def get(self, request):
        return HttpResponse("GET /view")


urlpatterns = router.urls


def test_func_decorators(client):
    response = client.get("/func")

    assert response.status_code == 200
    assert response.content == b"GET /func"
    assert response["x-after"] == "func2 func1 router2 router1"


def test_view_decorators(client):
    response = client.get("/view")

    assert response.status_code == 200
    assert response.content == b"GET /view"
    assert response["x-after"] == "view2 view1 router2 router1"
