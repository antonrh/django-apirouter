from apirouter import APIRouter
from django.http import HttpResponse

router = APIRouter()


@router.route("/")
def index(request):
    return HttpResponse


urlpatterns = router.urls
