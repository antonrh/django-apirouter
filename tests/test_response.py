from apirouter.response import JsonResponse, Response


def test_response_headers():
    response = Response(headers={"x-header": "test"})

    assert response["x-header"] == "test"


def test_json_response_headers():
    response = JsonResponse(None, headers={"x-header": "test"})

    assert response["x-header"] == "test"
