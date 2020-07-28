from functools import wraps
from typing import Callable, List, Optional, Type, Union, cast

import attr
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.urls import include
from django.urls import path as url_path
from django.urls.resolvers import URLPattern
from django.utils.decorators import decorator_from_middleware
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.views import View
from django.views.decorators.http import require_http_methods

from apirouter.decorators import compose_decorators
from apirouter.exception_handler import exception_handler as default_exception_handler
from apirouter.request import Request
from apirouter.response import JsonResponse
from apirouter.utils import removeprefix


@attr.s(auto_attribs=True)
class APIViewFuncRoute:
    path: str
    view_func: Callable
    name: Optional[str] = None
    methods: Optional[List[str]] = None


@attr.s(auto_attribs=True)
class APIViewClassRoute:
    path: str
    view_class: Type[View]
    name: Optional[str] = None
    decorators: Optional[List[Callable]] = None


@attr.s(auto_attribs=True)
class APIIncludeRoute:
    router: "APIRouter"
    prefix: str = ""


APIRouteType = Union[APIViewFuncRoute, APIViewClassRoute, APIIncludeRoute]
ExceptionHandlerType = Callable[[Request, Exception], HttpResponse]


class APIRouter:
    def __init__(
        self,
        *,
        name: Optional[str] = None,
        middleware_classes: Optional[List[Callable]] = None,
        exception_handler: Optional[ExceptionHandlerType] = None,
        request_class: Optional[Type[Request]] = None,
    ):
        self.name = name
        self.middleware_classes = middleware_classes or []
        self.exception_handler = (
            exception_handler or self._get_default_exception_handler()
        )
        self.request_class = request_class or self._get_default_request_class()
        self.routes: List[APIRouteType] = []

    @cached_property
    def middleware_decorators(self) -> List[Callable]:
        return [
            decorator_from_middleware(middleware_class)
            for middleware_class in reversed(self.middleware_classes)
        ]

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

        if isinstance(route, APIViewClassRoute):
            view_func = route.view_class.as_view()
            if route.decorators:
                view_func = compose_decorators(route.decorators)(view_func)
        else:
            view_func = route.view_func
            if route.methods:
                view_func = require_http_methods(route.methods)(route.view_func)

        @wraps(view_func)
        def wrapped_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            wrapped_request = self.request_class(request)
            try:
                response = view_func(wrapped_request, *args, **kwargs)
                if not isinstance(response, HttpResponse):
                    return JsonResponse(response)
                return response
            except Exception as exc:
                return self.exception_handler(wrapped_request, exc)

        return compose_decorators(*self.middleware_decorators)(wrapped_view)

    def _get_default_exception_handler(self) -> ExceptionHandlerType:
        exception_handler: Union[str, ExceptionHandlerType] = getattr(
            settings, "APIROUTER_DEFAULT_EXCEPTION_HANDLER", default_exception_handler
        )
        if isinstance(exception_handler, str):
            exception_handler = cast(
                ExceptionHandlerType, import_string(exception_handler)
            )
        return exception_handler

    def _get_default_request_class(self) -> Type[Request]:
        request_class: Union[str, Type[Request]] = getattr(
            settings, "APIROUTER_DEFAULT_REQUEST_CLASS", Request
        )
        if isinstance(request_class, str):
            request_class = cast(Type[Request], import_string(request_class))
        return request_class
