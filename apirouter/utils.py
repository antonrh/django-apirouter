from typing import Optional

from django.http import HttpResponse


def removeprefix(string: str, *, prefix: str):
    if string.startswith(prefix):
        start = len(prefix)
        return string[start:]
    return string


def set_response_headers(
    response: HttpResponse, headers: Optional[dict] = None
) -> None:
    if headers:
        for name, value in headers.items():
            response[name] = value
