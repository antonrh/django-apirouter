from typing import Type, Union, cast

from django.conf import settings
from django.http import HttpResponse
from django.utils.module_loading import import_string

from apirouter.exception_handler import exception_handler as default_exception_handler
from apirouter.request import Request
from apirouter.response import JsonResponse
from apirouter.types import ExceptionHandlerType


def get_default_exception_handler() -> ExceptionHandlerType:
    exception_handler: Union[str, ExceptionHandlerType] = getattr(
        settings, "APIROUTER_DEFAULT_EXCEPTION_HANDLER", default_exception_handler
    )
    if isinstance(exception_handler, str):
        exception_handler = cast(ExceptionHandlerType, import_string(exception_handler))
    return exception_handler


def get_default_request_class() -> Type[Request]:
    request_class: Union[str, Type[Request]] = getattr(
        settings, "APIROUTER_DEFAULT_REQUEST_CLASS", Request
    )
    if isinstance(request_class, str):
        request_class = cast(Type[Request], import_string(request_class))
    return request_class


def get_default_response_class() -> Type[HttpResponse]:
    response_class: Union[str, Type[HttpResponse]] = getattr(
        settings, "APIROUTER_DEFAULT_RESPONSE_CLASS", JsonResponse
    )
    if isinstance(response_class, str):
        response_class = cast(Type[HttpResponse], import_string(response_class))
    return response_class
