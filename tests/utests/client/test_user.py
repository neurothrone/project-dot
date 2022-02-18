from http import HTTPStatus

from .. import BaseClientTestCase


class ClientUserTestCase(BaseClientTestCase):
    def test_user_signup(self):
        payload = dict(
            email="jane.doe@email.com",
            username="janedoe",
            password="1234abcd",
            password2="1234abcd",

        )

        response = self.client.get("/auth/join",
                                   follow_redirects=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.client.post("/auth/join",
                                    data=payload,
                                    follow_redirects=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
