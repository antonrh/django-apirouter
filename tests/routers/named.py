from django.http import HttpResponse

from apirouter import APIRouter

router = APIRouter()


@router.get("/a", name="a")
def named_a(request):
    return HttpResponse("GET /named/a")


@router.get("/b", name="b")
def named_b(request):
    return HttpResponse("GET /named/b")


xyz_router = APIRouter(name="xyz")


@xyz_router.get("/x", name="x")
def named_x(request):
    return HttpResponse("GET /named/xyz/x")


@xyz_router.get("/y", name="y")
def named_y(request):
    return HttpResponse("GET /named/xyz/y")


@xyz_router.get("/z", name="z")
def named_z(request):
    return HttpResponse("GET /named/xyz/z")


router.include_router(xyz_router, prefix="/xyz/")
