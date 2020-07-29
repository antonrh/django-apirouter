from typing import Any, Type, TypeVar

from django.conf import settings
from django.http import HttpResponse
from django.utils.module_loading import import_string

from apirouter.exception_handler import exception_handler as default_exception_handler
from apirouter.request import Request
from apirouter.response import JsonResponse
from apirouter.types import ExceptionHandlerType

T = TypeVar("T")


def import_setting(setting_name: str, default: Any) -> Any:
    target = getattr(settings, setting_name, default)
    if isinstance(target, str):
        return import_string(target)
    return target


def get_default_exception_handler() -> ExceptionHandlerType:
    return import_setting(
        setting_name="APIROUTER_DEFAULT_EXCEPTION_HANDLER",
        default=default_exception_handler,
    )


def get_default_request_class() -> Type[Request]:
    return import_setting(
        setting_name="APIROUTER_DEFAULT_REQUEST_CLASS", default=Request
    )


def get_default_response_class() -> Type[HttpResponse]:
    return import_setting(
        setting_name="APIROUTER_DEFAULT_RESPONSE_CLASS", default=JsonResponse
    )
