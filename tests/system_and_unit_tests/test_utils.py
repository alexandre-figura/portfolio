import subprocess

import pytest

from portfolio import utils


def test_convert_rst_document_to_html():
    html = utils.rst_to_html('test')
    assert '<p>test</p>' in html


class TestGetUrlFromName:
    def test_caracters_are_converted_to_lowercase(self):
        name = 'ITEM'
        current_url = utils.get_url_from_name(name)
        expected_url = 'item'
        assert current_url == expected_url

    def test_spaces_are_replaced_by_underscores(self):
        name = 'item name'
        current_url = utils.get_url_from_name(name)
        expected_url = 'item_name'
        assert current_url == expected_url


class TestExtendedFlatPages:
    def test_get_pages_without_wildcard_in_path(self, app):
        page = utils.ExtendedFlatPages(app).get('projects/project 1')
        assert page.path == 'projects/project 1'

    def test_get_pages_with_wildcard_in_path(self, app):
        pages = utils.ExtendedFlatPages(app).get('projects/*')
        current_paths = sorted(page.path for page in pages)
        expected_paths = ['projects/project {}'.format(i) for i in range(1, 3)]
        assert current_paths == expected_paths


class TestWatchSassStylesheets:
    sass_folder = 'assets/sass'
    css_folder = 'static/css'

    def test_sass_is_called_with_the_right_parameters(self, mocker):
        mocker.patch('subprocess.call')
        utils.watch_sass_stylesheets(self.sass_folder, self.css_folder)
        current_command_line = ' '.join(subprocess.call.call_args[0][0])
        expected_command_line = 'sass --watch {}:{} --style expanded'\
                                .format(self.sass_folder, self.css_folder)
        assert current_command_line == expected_command_line

    def test_error_is_raised_when_sass_is_not_installed(self, mocker):
        mocker.patch('subprocess.call', side_effect=FileNotFoundError)

        with pytest.raises(FileNotFoundError) as excinfo:
            utils.watch_sass_stylesheets(self.sass_folder, self.css_folder)

        assert 'not installed' in str(excinfo.value)
