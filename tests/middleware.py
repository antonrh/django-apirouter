from django.utils.deprecation import MiddlewareMixin


class TestMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response["x-middleware-test"] = "yes"
        return response
