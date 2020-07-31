from typing import Callable, List, Optional, Type

from django.views import View

from apirouter.types import RequestType


def compose_decorators(*decorators):
    def decorator(func):
        for dec in reversed(decorators):
            func = dec(func)
        return func

    return decorator


def route(*, request_class: Optional[RequestType] = None):
    def decorator(view_func: Callable):
        setattr(view_func, "__apirouter_request_class", request_class)
        return view_func

    return decorator


def view(
    *,
    decorators: Optional[List[Callable]] = None,
    request_class: Optional[RequestType] = None,
):
    def decorator(view_class: Type[View]):
        setattr(view_class, "__apirouter_decorators", decorators)
        setattr(view_class, "__apirouter_request_class", request_class)
        return view_class

    return decorator
