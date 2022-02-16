from http import HTTPStatus

from .. import BaseClientTestCase


class ClientOpenTestCase(BaseClientTestCase):
    def test_index_route(self):
        response = self.client.get("/",
                                   follow_redirects=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue("Search for Developers" in
                        response.get_data(as_text=True))
