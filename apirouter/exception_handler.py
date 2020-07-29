from http import HTTPStatus

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse

from apirouter.exceptions import APIException
from apirouter.request import Request
from apirouter.response import JsonResponse


def exception_handler(request: Request, exc: Exception) -> HttpResponse:
    if isinstance(exc, Http404):
        exc = APIException(status_code=HTTPStatus.NOT_FOUND)
    elif isinstance(exc, PermissionDenied):
        exc = APIException(status_code=HTTPStatus.FORBIDDEN)

    if isinstance(exc, APIException):
        return JsonResponse(
            {"detail": exc.detail}, status=exc.status_code, headers=exc.headers
        )
    raise exc
