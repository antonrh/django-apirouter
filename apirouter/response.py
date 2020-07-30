from typing import Any, Optional, Union

from django.http.response import HttpResponse, JsonResponse as DjangoJsonResponse
from django.utils.encoding import force_bytes

from apirouter.utils import set_response_headers


class Response(HttpResponse):
    def __init__(
        self,
        content: Union[str, bytes] = b"",
        headers: Optional[dict] = None,
        *args,
        **kwargs
    ):
        super().__init__(force_bytes(content), *args, **kwargs)

        set_response_headers(self, headers)


class JsonResponse(DjangoJsonResponse):
    def __init__(self, data: Any, headers: Optional[dict] = None, **kwargs):
        kwargs["safe"] = False
        super().__init__(data, **kwargs)

        set_response_headers(self, headers)
