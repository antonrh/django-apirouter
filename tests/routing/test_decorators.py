from typing import Callable, List

import pytest
from django.http import HttpRequest, HttpResponse

from apirouter import APIRouter

pytestmark = [pytest.mark.urls(__name__)]


def append_request_before(request: HttpRequest, item: str) -> str:
    items: List[str] = getattr(request, "_before", "").split()
    items.append(item)
    items_str = " ".join(items)
    setattr(request, "_before", items_str)
    return items_str


def append_response_after(response: HttpResponse, item: str) -> str:
    response.setdefault("x-after-view", "")
    items: List[str] = response["x-after-view"].split()
    items.append(item)
    items_str = " ".join(items)
    response["x-after-view"] = items_str
    return items_str


def make_decorator(key: str):
    def decorator(view_func: Callable):
        def wrapped(request, *args, **kwargs):
            before = append_request_before(request, key)
            response = view_func(request, *args, **kwargs)
            response["x-before-view"] = before
            append_response_after(response, key)
            return response

        return wrapped

    return decorator


router = APIRouter(decorators=[make_decorator("global")])


@router.get("/decorator")
def decorator_get(request):
    return HttpResponse("GET /decorator")


urlpatterns = router.urls


def test_global_decorator_get(client):
    response = client.get("/decorator")

    assert response.status_code == 200
    assert response.content == b"GET /decorator"
    assert response["x-before-view"] == "global"
    assert response["x-after-view"] == "global"
