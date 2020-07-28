import pytest
from django.http import HttpResponse

from apirouter import APIRouter
from apirouter.exceptions import APIException

pytestmark = [pytest.mark.urls(__name__)]


def exception_handler(request, exc):
    return HttpResponse(str(exc), status=400)


router = APIRouter(exception_handler=exception_handler)


@router.get("/string")
def handle_string(request):
    return "OK"


@router.get("/dict")
def handle_dict(request):
    return {"success": True}


@router.get("/list")
def handle_list(request):
    return [1, 2, 3, 4, 5]


@router.get("/error")
def handle_error(request):
    raise APIException(status_code=400, detail="Error")


urlpatterns = router.urls


def test_handle_string(client):
    response = client.get("/string")

    assert response.status_code == 200
    assert response.json() == "OK"


def test_handle_dict(client):
    response = client.get("/dict")

    assert response.status_code == 200
    assert response.json() == {"success": True}


def test_handle_list(client):
    response = client.get("/list")

    assert response.status_code == 200
    assert response.json() == [1, 2, 3, 4, 5]


def test_handle_error(client):
    response = client.get("/error")

    assert response.status_code == 400
    assert response.content == b"Error"
