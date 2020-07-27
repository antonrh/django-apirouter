from django.http import HttpResponse

from apirouter.exceptions import APIException
from apirouter.request import Request
from apirouter.response import JsonResponse


def exception_handler(request: Request, exc: Exception) -> HttpResponse:
    if isinstance(exc, APIException):
        return JsonResponse(
            {"detail": exc.detail}, status=exc.status_code, headers=exc.headers
        )
    raise exc
