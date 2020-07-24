from django.http import HttpResponse

from apirouter.request import Request


def exception_handler(request: Request, exc: Exception) -> HttpResponse:
    return HttpResponse("ERROR")
