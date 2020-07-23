from collections import defaultdict
from dataclasses import dataclass, field
from functools import wraps
from typing import Callable, Dict, List, Optional, Tuple, Union

from django.core.exceptions import ImproperlyConfigured
from django.urls import include
from django.urls import path as url_path
from django.urls.resolvers import URLPattern
from django.utils.functional import cached_property
from django.views.decorators.http import require_http_methods

from apirouter.utils import http_method_dispatch


@dataclass
class RouteMixin:
    path: str
    func: Callable
    name: Optional[str] = None


@dataclass
class Route(RouteMixin):
    method: str = "GET"


@dataclass
class DispatchRoute(RouteMixin):
    methods: List[str] = field(default_factory=lambda: ["GET"])


@dataclass
class IncludeRoute:
    router: "Router"
    prefix: Optional[str] = None


RouteType = Union[Route, DispatchRoute, IncludeRoute]


class Router:
    def __init__(self, *, name: Optional[str] = None):
        self.name = name
        self._routes: List[RouteType] = []

    def include_router(self, router: "Router", *, prefix: Optional[str] = None) -> None:
        if prefix and prefix.startswith("/"):
            raise ImproperlyConfigured("A path prefix must not start with '/'")
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
            route = Route(path=path, func=func, name=name, method=methods[0])
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
        if path.startswith("/"):
            path = path[1:]  # remove prefix

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
    def urls(self) -> Union[Tuple[List[URLPattern], str], List[URLPattern]]:
        urls = self._build_urls()
        if self.name:
            return urls, self.name
        return urls

    def _build_urls(self) -> List[URLPattern]:
        ordered: Dict[str, URLPattern] = {}
        routes: Dict[str, List[Route]] = defaultdict(list)

        for route in self._routes:
            if isinstance(route, Route):
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
                ordered[route.prefix] = url_path(
                    route.prefix, include(route.router.urls)
                )

        return list(ordered.values())

    def _handle_view(self, func: Callable):
        @wraps(func)
        def inner(request, *args, **kwargs):
            return func(request, *args, **kwargs)

        return inner
