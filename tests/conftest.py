import pytest

from portfolio.utils import create_app


@pytest.fixture
def app():
    instance = create_app(TESTING=True)
    return instance
