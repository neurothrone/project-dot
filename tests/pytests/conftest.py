import pytest

from app import create_app
from app.config import ConfigType


@pytest.fixture(scope="function")
def app():
    app = create_app(ConfigType.TESTING)
    with app.app_context():
        yield app


@pytest.fixture(scope="function")
def client(app):
    with app.test_client() as client:
        yield client
