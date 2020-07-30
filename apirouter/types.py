from typing import Callable, Union

from django.http import HttpRequest, HttpResponse

from apirouter.request import Request

RequestType = Union[HttpRequest, Request]
ExceptionHandlerType = Callable[[RequestType, Exception], HttpResponse]
