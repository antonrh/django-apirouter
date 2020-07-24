from django.http import HttpRequest


class Request:
    def __init__(self, request: HttpRequest):
        self._request = request
