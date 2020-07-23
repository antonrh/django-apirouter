from django.http import HttpResponse

from apirouter import APIRouter

router = APIRouter()


@router.get("/")
def inner_list(request):
    return HttpResponse("GET /inner/")


@router.post("/")
def inner_create(request):
    return HttpResponse("POST /inner/")


@router.get("/<int:inner_id>/")
def inner_detail(request, inner_id: int):
    return HttpResponse(f"GET /inner/{inner_id}/")
