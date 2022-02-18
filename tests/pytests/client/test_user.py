from http import HTTPStatus


def test_user_join(client):
    payload = dict(
        email="jane.doe@email.com",
        username="janedoe",
        password="1234abcd",
        password2="1234abcd",

    )

    response = client.get("/auth/join", follow_redirects=True)
    assert response.status_code == HTTPStatus.OK

    response = client.post("/auth/join",
                           data=payload,
                           follow_redirects=True)
    assert response.status_code == HTTPStatus.OK
