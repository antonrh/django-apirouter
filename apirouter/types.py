from typing import Callable

from django.http import HttpResponse

from apirouter.request import Request

ExceptionHandlerType = Callable[[Request, Exception], HttpResponse]
