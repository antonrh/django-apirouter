def test_root_GET(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.content == b"GET /"


def test_root_POST(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.content == b"GET /"


def test_root_not_allowed(client):
    response = client.delete("/")

    assert response.status_code == 405
    assert response["Allow"] == "GET, POST"
