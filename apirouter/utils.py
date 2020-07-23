from typing import Callable, Dict

from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed


def http_method_dispatch(**method_handlers: Dict[str, Callable]) -> Callable:
    def not_allowed_method(
        request: HttpRequest, *args, **kwargs  # noqa
    ) -> HttpResponse:
        return HttpResponseNotAllowed(method_handlers.keys())

    def dispatch(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        handler = method_handlers.get(request.method, not_allowed_method)
        return handler(request, *args, **kwargs)

    return dispatch


def removeprefix(string: str, *, prefix: str):
    if string.startswith(prefix):
        start = len(prefix)
        return string[start:]
    return string
