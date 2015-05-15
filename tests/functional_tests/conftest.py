import pytest
import selenium.webdriver


@pytest.fixture(scope='module')
def browser(request):
    firefox = selenium.webdriver.Firefox()
    request.addfinalizer(lambda: firefox.quit())
    return firefox
