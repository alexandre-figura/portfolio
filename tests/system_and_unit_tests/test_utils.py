import subprocess

from portfolio import utils


def test_watch_sass_stylesheets(mocker):
    sass_folder = 'assets/sass'
    css_folder = 'static/css'

    mocker.patch('subprocess.call')
    utils.watch_sass_stylesheets('assets/sass', 'static/css')
    command_line = ' '.join(subprocess.call.call_args[0][0])

    assert command_line == 'sass --watch {}:{} --style expanded'.format(sass_folder, css_folder)
