from django.http import HttpResponse

from apirouter import APIRouter

router = APIRouter()


@router.route("/", methods=["GET", "POST"])
def root(request):
    return HttpResponse(f"{request.method} /")
