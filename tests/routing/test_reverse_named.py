import pytest
from django.test import override_settings
from django.urls import reverse

from apirouter import APIRouter

router = APIRouter(name="named")


@router.get("/", name="index")
def index(request):
    return


@router.get("/<int:param>", name="detail")
def detail(request, param: int):
    return


inner_router = APIRouter(name="inner")


@inner_router.get("/get", name="get")
def inner_get(request):
    return


router.include_router(inner_router, prefix="/inner/")


urlpatterns = router.urls


@override_settings(ROOT_URLCONF=__name__)
@pytest.mark.parametrize(
    "viewname,args,kwargs,expected",
    [
        ("named:index", [], {}, "/"),
        ("named:detail", [], {"param": 999}, "/999"),
        ("named:inner:get", [], {}, "/inner/get"),
    ],
)
def test_reverse_urls(viewname: str, args: list, kwargs: dict, expected: str):
    assert reverse(viewname, args=args, kwargs=kwargs) == expected
