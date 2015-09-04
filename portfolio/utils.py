from docutils.core import publish_parts
import subprocess

from flask_flatpages import FlatPages


class ExtendedFlatPages(FlatPages):
    def get(self, path, *args, **kwargs):
        if path.endswith('*'):
            path = path[:-1]
            pages = [page
                     for page_path, page in self._pages.items()
                     if page_path.startswith(path)]
            return pages
        return super().get(path, *args, **kwargs)


def get_url_from_name(name):
    url = name.lower().replace(' ', '_')
    return url


def rst_to_html(text):
    return publish_parts(text, writer_name='html')['html_body']


def watch_sass_stylesheets(sass_folder, css_folder, output_style='expanded'):
    """Run the Sass watcher to automatically update CSS stylesheets
    from their Sass sources.

    :param sass_folder: folder path where are stored the Sass source files.
    :param css_folder: folder path where will be generated the CSS
                       stylesheets.
    :param output_style: the style (e.g., expanded, compressed) used by Sass
                         to generate the CSS stylesheet.
    :raise FileNotFoundError: when the Sass program is not installed.
    """
    try:
        subprocess.call(
            [
                'sass',
                '--watch', '{}:{}'.format(sass_folder, css_folder),
                '--style', output_style,
            ],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError as e:
        raise FileNotFoundError('Sass is not installed') from e
