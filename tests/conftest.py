import os.path

import pytest

from portfolio.helpers import create_app


@pytest.fixture
def app():
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    pages_dir = os.path.sep.join((tests_dir, '/pages'))

    instance = create_app(
        TESTING=True,
        FLATPAGES_ROOT=pages_dir,
    )
    return instance
