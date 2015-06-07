import os
from pathlib import Path

import sass


def auto_reload_css(app, sass_folder, css_folder, sass_format='scss', output_style='expanded'):
    """Add a new view to a Flask application for serving CSS stylesheets.

    When the requested stylesheet has an associated Sass source file, then this last is compiled and sent in response.
    The compilation happens only if the source is more recent than the stylesheet.

    :param app: the Flask application.
    :param sass_folder: folder path where are stored the Sass sources.
                        If not absolute, this is relative to the :attr:`~Flask.root_path`.
    :param css_folder: folder path where are stored the CSS stylesheets.
                       Relative to the :attr:`~Flask.static_path`.
    :param sass_format: the syntax of Sass source files (e.g., scss, sass).
    :param output_style: the style (e.g., expanded, compressed) used by Sass to generate the CSS stylesheet.
    """
    if not os.path.isabs(sass_folder):
        sass_folder = os.path.join(app.root_path, sass_folder)
    sass_extension = '.{}'.format(sass_format)

    @app.route('{}/{}/<stylesheet>.css'.format(app.static_url_path, css_folder))
    def static_css(stylesheet):
        stylesheet += '.css'
        css_file = Path(app.static_folder, css_folder, stylesheet)
        scss_file = Path(sass_folder, stylesheet).with_suffix(sass_extension)

        if scss_file.exists():
            if not css_file.exists() or (css_file.stat().st_mtime < scss_file.stat().st_mtime):
                with css_file.open('w') as f:
                    f.write(
                        sass.compile(filename=str(scss_file), output_style=output_style),
                    )

        return app.send_static_file('{}/{}'.format(css_folder, stylesheet))
