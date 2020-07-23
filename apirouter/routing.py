from collections import defaultdict
from dataclasses import dataclass, field
from functools import wraps
from typing import Callable, Dict, List, Optional, Tuple, Union

from django.urls import include
from django.urls import path as url_path
from django.urls.resolvers import URLPattern
from django.utils.functional import cached_property
from django.views.decorators.http import require_http_methods

from apirouter.utils import http_method_dispatch, removeprefix


@dataclass
class RouteMixin:
    path: str
    func: Callable
    name: Optional[str] = None


@dataclass
class APIRoute(RouteMixin):
    method: str = "GET"


@dataclass
class DispatchRoute(RouteMixin):
    methods: List[str] = field(default_factory=lambda: ["GET"])


@dataclass
class IncludeRoute:
    router: "APIRouter"
    prefix: str = ""


RouteType = Union[APIRoute, DispatchRoute, IncludeRoute]


class APIRouter:
    def __init__(self, *, name: Optional[str] = None):
        self.name = name
        self._routes: List[RouteType] = []

    def include_router(self, router: "APIRouter", *, prefix: str = "") -> None:
        if prefix:
            prefix = removeprefix(prefix, prefix="/")
        self._routes.append(IncludeRoute(router=router, prefix=prefix))

    def add_route(
        self,
        path: str,
        func: Callable,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
    ) -> None:
        methods = methods or ["GET"]
        if len(methods) == 1:
            route = APIRoute(path=path, func=func, name=name, method=methods[0])
        else:
            route = DispatchRoute(path=path, func=func, name=name, methods=methods)
        self._routes.append(route)

    def route(
        self,
        path: str,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
    ) -> Callable:
        path = removeprefix(path, prefix="/")

        def decorator(func: Callable):
            self.add_route(path, func, methods=methods, name=name)
            return func

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

    @cached_property
    def urls(self) -> List[URLPattern]:
        urls = self._build_urls()
        if self.name:
            return [url_path("", include((urls, self.name)))]
        return urls

    def _build_urls(self) -> List[URLPattern]:
        ordered: Dict[str, URLPattern] = {}
        routes: Dict[str, List[APIRoute]] = defaultdict(list)

        for route in self._routes:
            if isinstance(route, APIRoute):
                routes[route.path].append(route)
                ordered[route.path] = url_path(
                    route.path,
                    view=http_method_dispatch(
                        **{
                            route.method: self._handle_view(route.func)
                            for route in routes[route.path]
                        }
                    ),
                )
            elif isinstance(route, DispatchRoute):
                ordered[route.path] = url_path(
                    route.path,
                    view=require_http_methods(route.methods)(
                        self._handle_view(route.func)
                    ),
                    name=route.name,
                )
            elif isinstance(route, IncludeRoute):
                ordered[route.prefix + str(id(route))] = url_path(
                    route.prefix, include(route.router.urls)
                )

        return list(ordered.values())

    def _handle_view(self, func: Callable):
        @wraps(func)
        def inner(request, *args, **kwargs):
            return func(request, *args, **kwargs)

        return inner
