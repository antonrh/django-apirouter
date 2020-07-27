import pytest

from apirouter import APIRouter

pytestmark = [pytest.mark.urls(__name__)]

router = APIRouter()


@router.get("/string")
def handle_string(request):
    return "OK"


@router.get("/dict")
def handle_dict(request):
    return {"success": True}


@router.get("/list")
def handle_list(request):
    return [1, 2, 3, 4, 5]


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
