import pytest
import webtest

from portfolio import PortfolioFlatPages


@pytest.fixture
def client(app):
    return webtest.TestApp(app)


@pytest.fixture
def flatpages(app):
    return PortfolioFlatPages(app)
