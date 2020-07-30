import json
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Union, cast

from django.contrib.sessions.backends.base import SessionBase
from django.core.files.uploadhandler import FileUploadHandler
from django.http import HttpRequest
from django.http.request import RAISE_ERROR, HttpHeaders, QueryDict
from django.urls import ResolverMatch
from django.utils.datastructures import MultiValueDict
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from apirouter.exceptions import APIException

if TYPE_CHECKING:
    from django.contrib.auth.models import AnonymousUser, User  # pragma: no cover

_missing = object()


class Request:
    """
    Request class.
    """

    def __init__(self, request: HttpRequest):
        self._request = request
        self._json: Optional[Any] = _missing

    def __getattr__(self, attr: str) -> Any:
        try:
            return getattr(self._request, attr)
        except AttributeError:
            return self.__getattribute__(attr)

    @property
    def query_params(self) -> QueryDict:
        """
        Returns dictionary-like HTTP GET parameters.
        """
        return cast(QueryDict, self._request.GET)

    @property
    def form(self) -> QueryDict:
        """
        Returns dictionary-like HTTP POST parameters.
        """
        return cast(QueryDict, self._request.POST)

    @property
    def files(self) -> MultiValueDict:
        """
        Returns dictionary-like object containing all uploaded files.
        """
        return cast(MultiValueDict, self._request.FILES)

    @property
    def cookies(self) -> Dict[str, str]:
        """
        Returns dictionary-like cookies. Keys and values are strings.
        """
        return self._request.COOKIES

    @property
    def path(self) -> str:
        return self._request.path

    @property
    def path_info(self) -> str:
        return self._request.path_info

    @property
    def method(self) -> str:
        return self._request.method

    @property
    def resolver_match(self) -> Optional[ResolverMatch]:
        return self._request.resolver_match

    @property
    def content_type(self) -> str:
        return self._request.content_type

    @property
    def content_params(self) -> dict:
        return self._request.content_params

    @cached_property
    def headers(self) -> HttpHeaders:
        return self._request.headers

    def get_host(self) -> str:
        return self._request.get_host()

    def get_port(self) -> str:
        return self._request.get_port()

    def get_full_path(self, force_append_slash: bool = False) -> str:
        return self._request.get_full_path(force_append_slash)

    def get_full_path_info(self, force_append_slash: bool = False) -> str:
        return self._request.get_full_path_info(force_append_slash)

    def get_signed_cookie(
        self,
        key: str,
        default=RAISE_ERROR,
        salt: str = "",
        max_age: Optional[int] = None,
    ) -> Any:
        return self._request.get_signed_cookie(
            key, default=default, salt=salt, max_age=max_age
        )

    def get_raw_uri(self) -> str:
        return self._request.get_raw_uri()

    def build_absolute_uri(self, location: Optional[str] = None) -> str:
        return self._request.build_absolute_uri(location)

    @property
    def scheme(self) -> str:
        return self._request.scheme

    def is_secure(self) -> bool:
        return self._request.is_secure()

    @property
    def encoding(self) -> str:
        return self._request.encoding

    @encoding.setter
    def encoding(self, encoding: str):
        self._request.encoding = encoding

    @property
    def upload_handlers(self) -> List[FileUploadHandler]:
        return self._request.upload_handlers

    @upload_handlers.setter
    def upload_handlers(self, upload_handlers: List[FileUploadHandler]) -> None:
        self._request.upload_handlers = upload_handlers

    @property
    def body(self) -> bytes:
        return self._request.body

    def parse_file_upload(self, META: Mapping, post_data: Mapping) -> Mapping:
        return self._request.parse_file_upload(META, post_data)

    def close(self) -> None:
        self._request.close()

    def read(self, *args, **kwargs):
        return self._request.read(*args, **kwargs)

    def readline(self, *args, **kwargs):
        self._request.readline(*args, **kwargs)

    def __iter__(self):
        return self._request.__iter__()

    def readlines(self) -> list:
        return self._request.readlines()

    def json(self) -> Any:
        """
        Get JSON content.
        """
        if self._json is _missing:
            try:
                self._json = json.loads(self.body)
            except ValueError:
                raise APIException(
                    status_code=HTTPStatus.BAD_REQUEST, detail=_("Invalid JSON body.")
                )
        return self._json

    @property
    def session(self) -> SessionBase:
        session = getattr(self._request, "session", None)
        if session is None:
            raise AttributeError(
                "To use session, please "
                "add `django.contrib.sessions` to INSTALLED_APPS and "
                "add `django.contrib.sessions.middleware.SessionMiddleware`"
            )
        return session

    @property
    def user(self) -> Union["User", "AnonymousUser"]:
        user = getattr(self._request, "user", None)
        if user is None:
            raise AttributeError(
                "To use user, please "
                "add `django.contrib.auth` to INSTALLED_APPS and "
                "add `django.contrib.auth.middleware.AuthenticationMiddleware`"
            )
        return user
