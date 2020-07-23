from collections import defaultdict
from typing import Callable, Dict, List, Optional

from django.urls import path as _path
from django.urls.resolvers import URLPattern
from django.utils.functional import cached_property
from django.views.decorators.http import require_http_methods

from apirouter.utils import method_dispatch


class APIRoute:
    def __init__(
        self,
        *,
        path: str,
        func: Callable,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
    ):
        self.path = path
        self.func = func
        self.methods = methods or ["GET"]
        self.name = name


class APIRouter:
    def __init__(self):
        self._routes: Dict[str, List[APIRoute]] = defaultdict(list)

    def add_route(
        self,
        path: str,
        func: Callable,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
    ) -> None:
        self._routes[path].append(
            APIRoute(path=path, func=func, methods=methods, name=name)
        )

    def route(
        self,
        path: str,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
    ) -> Callable:
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
        return self._build_urls()

    def _build_urls(self) -> List[URLPattern]:
        ret = []
        for path, routes in self._routes.items():
            if not routes:
                continue

            if len(routes) > 1:
                ret.append(
                    _path(
                        path,
                        view=method_dispatch(
                            **{
                                route.methods[0]: route.func
                                for route in routes
                                if route.methods
                            }
                        ),
                    )
                )
            else:
                route = routes[0]
                ret.append(
                    _path(
                        route.path,
                        view=require_http_methods(route.methods)(route.func),
                        name=route.name,
                    )
                )
        return ret
