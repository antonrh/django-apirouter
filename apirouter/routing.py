from dataclasses import dataclass
from typing import Callable, List, Optional, Type, Union

from django.urls import include
from django.urls import path as url_path
from django.urls.resolvers import URLPattern
from django.utils.decorators import decorator_from_middleware
from django.utils.functional import cached_property
from django.views import View
from django.views.decorators.http import require_http_methods

from apirouter.utils import compose_decorators, removeprefix


@dataclass
class APIViewFuncRoute:
    path: str
    view_func: Callable
    name: Optional[str] = None
    methods: Optional[List[str]] = None


@dataclass
class APIViewClassRoute:
    path: str
    view_class: Type[View]
    name: Optional[str] = None
    decorators: Optional[List[Callable]] = None


@dataclass
class APIIncludeRoute:
    router: "APIRouter"
    prefix: str = ""


APIRouteType = Union[APIViewFuncRoute, APIViewClassRoute, APIIncludeRoute]


class APIRouter:
    def __init__(
        self, *, name: Optional[str] = None, middleware: Optional[List[Callable]] = None
    ):
        self.name = name
        self.middleware = middleware or []
        self.routes: List[APIRouteType] = []

    @cached_property
    def middleware_decorators(self) -> List[Callable]:
        return [decorator_from_middleware(middleware) for middleware in self.middleware]

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
    ):
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
        urls: List[URLPattern] = []

        for route in self.routes:
            if isinstance(route, APIIncludeRoute):
                urls.append(url_path(route.prefix, include(route.router.urls)))
            else:
                urls.append(
                    url_path(route.path, view=self._handle(route), name=route.name)
                )

        return urls

    def _handle(self, route: Union[APIViewFuncRoute, APIViewClassRoute]) -> Callable:
        if isinstance(route, APIViewClassRoute):
            view_func = route.view_class.as_view()
        else:
            if route.methods:
                view_func = require_http_methods(route.methods)(route.view_func)
            else:
                view_func = route.view_func
        return compose_decorators(*self.middleware_decorators)(view_func)
