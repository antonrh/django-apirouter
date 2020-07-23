from django.http import HttpResponse

from apirouter import APIRouter

router = APIRouter()


@router.route("method/", methods=["GET", "POST"])
def method(request):
    return HttpResponse(f"METHOD {request.method}")


@router.get("dispatch/")
def dispatch_get(request):
    return HttpResponse("DISPATCH GET")


@router.post("dispatch/")
def dispatch_post(request):
    return HttpResponse("DISPATCH POST")
