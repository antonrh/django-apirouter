from apirouter.exceptions import APIException


def test_api_exception_detail():
    exc = APIException(400)

    assert exc.detail == "Bad Request"
