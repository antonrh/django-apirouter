from django.http import HttpResponse

from apirouter import APIRouter

router = APIRouter()


@router.get("/method")
def method_get(request):
    return HttpResponse("GET /method")


@router.put("/method")
def method_put(request):
    return HttpResponse("PUT /method")


@router.post("/method")
def method_post(request):
    return HttpResponse("POST /method")


@router.delete("/method")
def method_delete(request):
    return HttpResponse("DELETE /method")


@router.options("/method")
def method_options(request):
    return HttpResponse("OPTIONS /method")


@router.head("/method")
def method_head(request):
    response = HttpResponse()
    response["content"] = "HEAD /method"
    return response


@router.patch("/method")
def method_patch(request):
    return HttpResponse("PATCH /method")


@router.trace("/method")
def method_trace(request):
    return HttpResponse("TRACE /method")
