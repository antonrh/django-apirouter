def test_method_GET(client):
    response = client.get("/method")

    assert response.status_code == 200
    assert response.content == b"GET /method"


def test_method_PUT(client):
    response = client.put("/method")

    assert response.status_code == 200
    assert response.content == b"PUT /method"


def test_method_POST(client):
    response = client.post("/method")

    assert response.status_code == 200
    assert response.content == b"POST /method"


def test_method_DELETE(client):
    response = client.delete("/method")

    assert response.status_code == 200
    assert response.content == b"DELETE /method"


def test_method_OPTIONS(client):
    response = client.get("/method")

    assert response.status_code == 200
    assert response.content == b"GET /method"


def test_method_HEAD(client):
    response = client.head("/method")

    assert response.status_code == 200
    assert response["content"] == "HEAD /method"


def test_method_PATCH(client):
    response = client.patch("/method")

    assert response.status_code == 200
    assert response.content == b"PATCH /method"


def test_method_TRACE(client):
    response = client.trace("/method")

    assert response.status_code == 200
    assert response.content == b"TRACE /method"
