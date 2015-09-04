import flask
import jinja2
import pytest

from portfolio import helpers

import portfolio


class TestApplicationFactory:
    def test_application_is_configured_accordingly_to_keyword_parameters(self):
        app = helpers.create_app(CONFIG_KEY_1='key1', CONFIG_KEY_2='key2')
        assert app.config['CONFIG_KEY_1'] == 'key1'
        assert app.config['CONFIG_KEY_2'] == 'key2'

    def test_extensions_are_initialized(self):
        app = helpers.create_app()
        assert portfolio.pages.app is app

    def test_jinja2_is_configured_to_not_silently_pass_undefined_variables(self):
        app = helpers.create_app()

        with pytest.raises(jinja2.exceptions.UndefinedError):
            with app.test_request_context():
                flask.render_template_string('{{ undefined_variable }}')
