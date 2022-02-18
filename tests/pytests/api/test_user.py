from http import HTTPStatus

from flask import Response

payload = dict(
    username="janedoe",
    email="jane.doe@email.com",
    password="1234abcd",
    password2="1234abcd",
)


def create_user_utility(client, data) -> Response:
    return client.post("/api/users", data=data)


def test_create_user(client):
    response = create_user_utility(client, payload)
    assert response.status_code == HTTPStatus.CREATED

    json = response.json
    assert json["username"] == payload["username"]
    assert json["email"] == payload["email"]
    assert json["id"] is not None


def test_read_users(client):
    for _ in range(5):
        create_user_utility(client, payload)

    response = client.get("/api/users")
    assert response.status_code == HTTPStatus.OK

    # pprint.pp(response.json)
    assert len(response.json) >= 5


def test_read_user(client):
    response = create_user_utility(client, payload)
    assert response.status_code == HTTPStatus.CREATED

    user_id = response.json["id"]
    assert user_id is not None

    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK

    json = response.json
    assert json["username"] == payload["username"]
    assert json["email"] == payload["email"]
    assert json["id"] is not None
