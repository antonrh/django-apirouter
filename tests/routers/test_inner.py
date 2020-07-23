def test_inner_list(client):
    response = client.get("/inner/")

    assert response.status_code == 200
    assert response.content == b"GET /inner/"


def test_inner_create(client):
    response = client.post("/inner/")

    assert response.status_code == 200
    assert response.content == b"POST /inner/"


def test_inner_detail(client):
    response = client.get("/inner/100/")

    assert response.status_code == 200
    assert response.content == b"GET /inner/100/"
