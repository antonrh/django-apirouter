from dataclasses import dataclass
from typing import Callable, List, Optional, Type, Union

from django.urls import include
from django.urls import path as url_path
from django.urls.resolvers import URLPattern
from django.utils.functional import cached_property
from django.views import View
from django.views.decorators.http import require_http_methods

from apirouter.utils import removeprefix


@dataclass
class APIRoute:
    path: str
    view: Union[Callable, Type[View]]
    name: Optional[str] = None
    methods: Optional[List[str]] = None


@dataclass
class IncludeRoute:
    router: "APIRouter"
    prefix: str = ""


RouteType = Union[APIRoute, IncludeRoute]


class APIRouter:
    def __init__(self, *, name: Optional[str] = None):
        self.name = name
        self.routes: List[RouteType] = []

    def include_router(self, router: "APIRouter", *, prefix: str = "") -> None:
        if prefix:
            prefix = removeprefix(prefix, prefix="/")
        self.routes.append(IncludeRoute(router=router, prefix=prefix))

    def add_route(
        self,
        path: str,
        func: Callable,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.routes.append(APIRoute(path=path, view=func, name=name, methods=methods))

    def add_view(self, path: str, view: Type[View], *, name: Optional[str] = None):
        self.routes.append(APIRoute(path=path, view=view, name=name))

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

    def view(self, path: str, *, name: Optional[str] = None) -> Callable:
        path = removeprefix(path, prefix="/")

        def decorator(view: Type[View]) -> Callable:
            self.add_view(path, view, name=name)
            return view

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
        urls: List[URLPattern] = []

        for route in self.routes:
            if isinstance(route, APIRoute):
                urls.append(
                    url_path(route.path, view=self._handle(route), name=route.name)
                )
            elif isinstance(route, IncludeRoute):
                urls.append(url_path(route.prefix, include(route.router.urls)))

        return urls

    def _handle(self, route: APIRoute):
        if isinstance(route.view, View):
            return route.view.as_view()
        else:
            if route.methods:
                return require_http_methods(route.methods)(route.view)
            return route.view
