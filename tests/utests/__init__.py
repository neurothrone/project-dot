import unittest

from app import create_app
from app.config import ConfigType


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(ConfigType.TESTING)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()


class BaseClientTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        # use_cookies=True is necessary for Flask-Login
        self.client = self.app.test_client(use_cookies=True)
