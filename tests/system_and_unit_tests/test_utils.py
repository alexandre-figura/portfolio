import subprocess

from portfolio import utils
import pytest


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
