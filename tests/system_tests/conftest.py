import pytest
import webtest


@pytest.fixture
def client(app):
    return webtest.TestApp(app)
