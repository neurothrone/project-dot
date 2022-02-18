from http import HTTPStatus


def test_open(client):
    response = client.get("/", follow_redirects=True)
    assert response.status_code == HTTPStatus.OK
    assert "Search for Developers" in response.get_data(as_text=True)
