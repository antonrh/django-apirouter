from dataclasses import dataclass, field
from functools import wraps
from typing import Callable, List, Optional, Type, Union

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
from apirouter.types import ExceptionHandlerType, RequestType
from apirouter.utils import removeprefix


@dataclass(frozen=True)
class APIViewFuncRoute:
    path: str
    view_func: Callable
    methods: Optional[List[str]] = None
    name: Optional[str] = None
    request_class: Optional[Type[RequestType]] = None

    def __post_init__(self):
        if self.methods:
            view_func = require_http_methods(self.methods)(self.view_func)
            object.__setattr__(self, "view_func", view_func)


@dataclass(frozen=True)
class APIViewClassRoute:
    path: str
    view_class: Type[View]
    view_func: Callable = field(init=False)
    name: Optional[str] = None
    decorators: Optional[List[Callable]] = None
    request_class: Optional[Type[RequestType]] = None

    def __post_init__(self):
        view_func = self.view_class.as_view()
        if self.decorators:
            view_func = compose_decorators(*self.decorators)(view_func)
        object.__setattr__(self, "view_func", view_func)


@dataclass(frozen=True)
class APIIncludeRoute:
    router: "APIRouter"
    prefix: str = ""


APIRoute = Union[APIViewFuncRoute, APIViewClassRoute]
APIRouteAny = Union[APIViewFuncRoute, APIViewClassRoute, APIIncludeRoute]


class APIRouter:
    def __init__(
        self,
        *,
        name: Optional[str] = None,
        decorators: Optional[List[Callable]] = None,
        exception_handler: Optional[ExceptionHandlerType] = None,
        request_class: Optional[Type[RequestType]] = None,
        response_class: Optional[Type[HttpResponse]] = None,
    ):
        self.name = name
        self.decorators = decorators or []
        self.exception_handler = exception_handler or get_default_exception_handler()
        self.request_class = request_class or get_default_request_class()
        self.response_class = response_class or get_default_response_class()
        self.routes: List[APIRouteAny] = []

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
        request_class: Optional[Type[RequestType]] = None,
    ) -> None:
        self.routes.append(
            APIViewFuncRoute(
                path=path,
                view_func=view_func,
                name=name,
                methods=methods,
                request_class=request_class,
            )
        )

    def add_view(
        self,
        path: str,
        view_class: Type[View],
        *,
        name: Optional[str] = None,
        decorators: Optional[List[Callable]] = None,
        request_class: Optional[Type[RequestType]] = None,
    ) -> None:
        self.routes.append(
            APIViewClassRoute(
                path=path,
                view_class=view_class,
                name=name,
                decorators=decorators,
                request_class=request_class,
            )
        )

    def route(
        self,
        path: str,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
        request_class: Optional[Type[RequestType]] = None,
    ) -> Callable:
        path = removeprefix(path, prefix="/")

        def decorator(view_func: Callable):
            self.add_route(
                path, view_func, methods=methods, name=name, request_class=request_class
            )
            return view_func

        return decorator

    def view(
        self,
        path: str,
        *,
        name: Optional[str] = None,
        decorators: Optional[List[Callable]] = None,
        request_class: Optional[Type[RequestType]] = None,
    ) -> Callable:
        path = removeprefix(path, prefix="/")

        def decorator(view_class: Type[View]) -> Callable:
            self.add_view(
                path,
                view_class,
                name=name,
                decorators=decorators,
                request_class=request_class,
            )
            return view_class

        return decorator

    def path(self, route: APIRoute) -> URLPattern:
        """
        Make route URL pattern.
        """
        return url_path(route.path, view=self._handle(route), name=route.name)

    def include(self, route: APIIncludeRoute) -> URLPattern:
        """
        Make include URL pattern.
        """
        return url_path(route.prefix, include(route.router.urls))

    def _build_urls(self) -> List[URLPattern]:
        """
        Build Django URL patterns sequence.
        """
        urlpatterns: List[URLPattern] = []

        for route in self.routes:
            if isinstance(route, APIIncludeRoute):
                urlpatterns.append(self.include(route))
            else:
                urlpatterns.append(self.path(route))

        return urlpatterns

    def _handle(self, route: APIRoute) -> Callable:
        """
        Handle route.
        """

        @wraps(route.view_func)
        def wrapped_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            request_class = route.request_class or self.request_class
            if issubclass(request_class, Request):
                request = request_class(request)
            try:
                get_response = compose_decorators(*self.decorators)(route.view_func)
                response = get_response(request, *args, **kwargs)
                if not isinstance(response, HttpResponse):
                    return self.response_class(response)
                return response
            except Exception as exc:
                return self.exception_handler(request, exc)

        return wrapped_view
