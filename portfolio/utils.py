import subprocess

from flask import Flask
import jinja2
from werkzeug.datastructures import ImmutableDict

from . import pages


def create_app(**kwargs):
    """Initialize and configure a Flask application from the given keyword arguments.

    :return: the configured Flask application.
    """
    # Initialize and configure Flask application.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('portfolio.default_settings')
    app.config.from_pyfile('portfolio.cfg', silent=True)
    app.config.update(kwargs)

    # In order to not partially render content of web pages,
    # the template engine must raise an exception for undefined variables.
    app.jinja_options = ImmutableDict(undefined=jinja2.StrictUndefined, **app.jinja_options)

    # Initialize extensions.
    pages.init_app(app)

    # Register Blueprints.
    from portfolio.views import website
    app.register_blueprint(website)

    return app


def watch_sass_stylesheets(sass_folder, css_folder, output_style='expanded'):
    """Run the Sass watcher to automatically update CSS stylesheets from their Sass sources.

    :param sass_folder: folder path where are stored the Sass source files.
    :param css_folder: folder path where will be generated the CSS stylesheets.
    :param output_style: the style (e.g., expanded, compressed) used by Sass to generate the CSS stylesheet.
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
