from typing import Callable, Dict

from django.http import HttpRequest, HttpResponseNotAllowed


def method_dispatch(**method_handlers: Dict[str, Callable]):
    def invalid_method(request: HttpRequest, *args, **kwargs):  # noqa
        return HttpResponseNotAllowed(method_handlers.keys())

    def dispatch(request: HttpRequest, *args, **kwargs):
        handler = method_handlers.get(request.method, invalid_method)
        return handler(request, *args, **kwargs)

    return dispatch
