from functools import wraps
from typing import Callable, List, Optional, Type, Union

import attr
from django.http import HttpRequest, HttpResponse
from django.urls import include, path as url_path
from django.urls.resolvers import URLPattern
from django.utils.functional import cached_property
from django.views import View
from django.views.decorators.http import require_http_methods

from apirouter.conf import (
    get_default_exception_handler,
    get_default_request_class,
    get_default_response_class,
)
from apirouter.decorators import compose_decorators
from apirouter.request import Request
from apirouter.types import ExceptionHandlerType
from apirouter.utils import removeprefix


@attr.s(auto_attribs=True, frozen=True)
class APIViewFuncRoute:
    path: str
    view_func: Callable
    name: Optional[str] = None
    methods: Optional[List[str]] = None

    def __attrs_post_init__(self):
        if self.methods:
            view_func = require_http_methods(self.methods)(self.view_func)
            object.__setattr__(self, "view_func", view_func)


@attr.s(auto_attribs=True, frozen=True)
class APIViewClassRoute:
    path: str
    view_class: Type[View]
    name: Optional[str] = None
    decorators: Optional[List[Callable]] = None
    view_func: Callable = attr.ib(init=False)

    def __attrs_post_init__(self):
        view_func = self.view_class.as_view()
        if self.decorators:
            view_func = compose_decorators(*self.decorators)(view_func)
        object.__setattr__(self, "view_func", view_func)


@attr.s(auto_attribs=True, frozen=True)
class APIIncludeRoute:
    router: "APIRouter"
    prefix: str = ""


APIRouteType = Union[APIViewFuncRoute, APIViewClassRoute, APIIncludeRoute]


class APIRouter:
    def __init__(
        self,
        *,
        name: Optional[str] = None,
        decorators: Optional[List[Callable]] = None,
        exception_handler: Optional[ExceptionHandlerType] = None,
        request_class: Optional[Type[Request]] = None,
        response_class: Optional[Type[HttpResponse]] = None,
    ):
        self.name = name
        self.decorators = decorators or []
        self.exception_handler = exception_handler or get_default_exception_handler()
        self.request_class = request_class or get_default_request_class()
        self.response_class = response_class or get_default_response_class()
        self.routes: List[APIRouteType] = []

    @cached_property
    def urls(self) -> List[URLPattern]:
        urls = self._build_urls()
        if self.name:
            return [url_path("", include((urls, self.name)))]
        return urls

    def include_router(self, router: "APIRouter", *, prefix: str = "") -> None:
        if prefix:
            prefix = removeprefix(prefix, prefix="/")
        self.routes.append(APIIncludeRoute(router=router, prefix=prefix))

    def add_route(
        self,
        path: str,
        view_func: Callable,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.routes.append(
            APIViewFuncRoute(path=path, view_func=view_func, name=name, methods=methods)
        )

    def add_view(
        self,
        path: str,
        view_class: Type[View],
        *,
        name: Optional[str] = None,
        decorators: Optional[List[Callable]] = None,
    ) -> None:
        self.routes.append(
            APIViewClassRoute(
                path=path, view_class=view_class, name=name, decorators=decorators
            )
        )

    def route(
        self,
        path: str,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
    ) -> Callable:
        path = removeprefix(path, prefix="/")

        def decorator(view_func: Callable):
            self.add_route(path, view_func, methods=methods, name=name)
            return view_func

        return decorator

    def view(
        self,
        path: str,
        *,
        name: Optional[str] = None,
        decorators: Optional[List[Callable]] = None,
    ) -> Callable:
        path = removeprefix(path, prefix="/")

        def decorator(view_class: Type[View]) -> Callable:
            self.add_view(path, view_class, name=name, decorators=decorators)
            return view_class

        return decorator

    def get(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["GET"], name=name)

    def put(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["PUT"], name=name)

    def post(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["POST"], name=name)

    def delete(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["DELETE"], name=name)

    def options(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["OPTIONS"], name=name)

    def head(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["HEAD"], name=name)

    def patch(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["PATCH"], name=name)

    def trace(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["TRACE"], name=name)

    def _build_urls(self) -> List[URLPattern]:
        """
        Build Django URL patterns sequence.
        """
        urlpatterns: List[URLPattern] = []

        for route in self.routes:
            if isinstance(route, APIIncludeRoute):
                urlpatterns.append(url_path(route.prefix, include(route.router.urls)))
            else:
                urlpatterns.append(
                    url_path(route.path, view=self._handle(route), name=route.name)
                )

        return urlpatterns

    def _handle(self, route: Union[APIViewFuncRoute, APIViewClassRoute]) -> Callable:
        """
        Handle route.
        """

        @wraps(route.view_func)
        def wrapped_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            wrapped_request = self.request_class(request)
            try:
                get_response = compose_decorators(*self.decorators)(route.view_func)
                response = get_response(wrapped_request, *args, **kwargs)
                if not isinstance(response, HttpResponse):
                    return self.response_class(response)
                return response
            except Exception as exc:
                return self.exception_handler(wrapped_request, exc)

        return wrapped_view
