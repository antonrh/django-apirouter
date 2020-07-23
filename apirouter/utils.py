from typing import Callable, Dict

from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed


def method_dispatch(**method_handlers: Dict[str, Callable]) -> Callable:
    def invalid_method(request: HttpRequest, *args, **kwargs) -> HttpResponse:  # noqa
        return HttpResponseNotAllowed(method_handlers.keys())

    def dispatch(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        handler = method_handlers.get(request.method, invalid_method)
        return handler(request, *args, **kwargs)

    return dispatch
