import pytest
import webtest

from portfolio import ExtendedFlatPages


@pytest.fixture
def client(app):
    return webtest.TestApp(app)


@pytest.fixture
def flatpages(app):
    return ExtendedFlatPages(app)
