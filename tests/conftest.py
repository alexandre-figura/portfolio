import pytest

from portfolio import portfolio


@pytest.fixture
def app():
    portfolio.app.config['TESTING'] = True
    return portfolio.app
