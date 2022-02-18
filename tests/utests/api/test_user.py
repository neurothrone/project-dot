from http import HTTPStatus

from flask.testing import FlaskClient

from .. import BaseClientTestCase

payload = dict(
    username="janedoe",
    email="jane.doe@email.com",
    password="1234abcd",
    password2="1234abcd",
)


class APIUserTestCase(BaseClientTestCase):
    @staticmethod
    def create_user(client: FlaskClient, data: dict):
        return client.post("/api/users", data=data)

    def test_create_user(self):
        response = APIUserTestCase.create_user(self.client, payload)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_read_users(self):
        for _ in range(5):
            response = APIUserTestCase.create_user(self.client, payload)
            self.assertEqual(response.status_code, HTTPStatus.CREATED)

        response = self.client.get("/api/users")
        assert response.status_code == HTTPStatus.OK

        json = response.json
        self.assertTrue(len(json) >= 5)

    def test_read_user(self):
        response = APIUserTestCase.create_user(self.client, payload)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        user_id = response.json.get("id")
        self.assertIsNotNone(user_id)

        response = self.client.get(f"/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK

        json = response.json

        self.assertEqual(json["username"], payload["username"])
        self.assertEqual(json["email"], payload["email"])
        self.assertIsNotNone(json["id"])
