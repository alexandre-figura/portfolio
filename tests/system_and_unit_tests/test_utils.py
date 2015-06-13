import subprocess

import flask
import jinja2
import pytest

import portfolio
from portfolio import utils


class TestApplicationFactory:
    def test_application_is_configured_accordingly_to_keyword_parameters(self):
        app = utils.create_app(CONFIG_KEY_1='key1', CONFIG_KEY_2='key2')
        assert app.config['CONFIG_KEY_1'] == 'key1'
        assert app.config['CONFIG_KEY_2'] == 'key2'

    def test_extensions_are_initialized(self):
        app = utils.create_app()
        assert portfolio.pages.app is app

    def test_jinja2_is_configured_to_not_silently_pass_undefined_variables(self):
        app = utils.create_app()

        with pytest.raises(jinja2.exceptions.UndefinedError):
            with app.test_request_context():
                flask.render_template_string('{{ undefined_variable }}')


class TestWatchSassStylesheets:
    sass_folder = 'assets/sass'
    css_folder = 'static/css'

    def test_sass_is_called_with_the_right_parameters(self, mocker):
        mocker.patch('subprocess.call')
        utils.watch_sass_stylesheets(self.sass_folder, self.css_folder)
        command_line = ' '.join(subprocess.call.call_args[0][0])

        assert command_line == 'sass --watch {}:{} --style expanded'.format(self.sass_folder, self.css_folder)

    def test_filenotfounderror_is_raised_when_sass_is_not_installed(self, mocker):
        mocker.patch('subprocess.call', side_effect=FileNotFoundError)

        with pytest.raises(FileNotFoundError) as excinfo:
            utils.watch_sass_stylesheets(self.sass_folder, self.css_folder)

        assert 'not installed' in str(excinfo.value)
