def test_method_GET(client):
    response = client.get("/method/")

    assert response.status_code == 200
    assert response.content == b"METHOD GET"


def test_method_POST(client):
    response = client.post("/method/")

    assert response.status_code == 200
    assert response.content == b"METHOD POST"


def test_method_not_allowed(client):
    response = client.delete("/method/")

    assert response.status_code == 405
    assert response["Allow"] == "GET, POST"


def test_dispatch_GET(client):
    response = client.get("/dispatch/")

    assert response.status_code == 200
    assert response.content == b"DISPATCH GET"


def test_dispatch_POST(client):
    response = client.post("/dispatch/")

    assert response.status_code == 200
    assert response.content == b"DISPATCH POST"


def test_dispatch_not_allowed(client):
    response = client.delete("/dispatch/")

    assert response.status_code == 405
    assert response["Allow"] == "GET, POST"
