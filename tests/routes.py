from django.http import HttpResponse
from django.views import View

from apirouter import APIRouter

router = APIRouter(name="root")


@router.route("/", name="index")
def root_index(request):
    return HttpResponse(f"{request.method} /")


@router.route("/method", name="method", methods=["GET", "POST"])
def root_method(request):
    return HttpResponse(f"{request.method} /method")


@router.get("/method/get", name="method_get")
def root_method_get(request):
    return HttpResponse("GET /get")


@router.put("/method/put", name="method_put")
def root_method_put(request):
    return HttpResponse("PUT /method/put")


@router.post("/method/post", name="method_post")
def root_method_post(request):
    return HttpResponse("POST /method/post")


@router.patch("/method/patch", name="method_patch")
def root_method_patch(request):
    return HttpResponse("PATCH /method/patch")


@router.delete("/method/delete", name="method_delete")
def root_method_delete(request):
    return HttpResponse("DELETE /method/delete")


@router.options("/method/options", name="method_options")
def root_method_options(request):
    return HttpResponse("OPTIONS /method/options")


@router.trace("/method/trace", name="method_trace")
def root_method_trace(request):
    return HttpResponse("TRACE /method/trace")


@router.head("/method/head", name="method_head")
def root_method_head(request):
    return HttpResponse("HEAD /method/head")


@router.view("/view", name="view")
class RootIndexView(View):
    def get(self, request):
        return HttpResponse("GET /view")

    def post(self, request):
        return HttpResponse("POST /view")
