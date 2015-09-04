from flask import Flask
import jinja2
from werkzeug.datastructures import ImmutableDict

from . import pages


def create_app(**kwargs):
    """Initialize and configure a Flask application
    from the given keyword arguments.

    :return: the configured Flask application.
    """
    # Initialize and configure Flask application.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('portfolio.default_settings')
    app.config.from_pyfile('portfolio.cfg', silent=True)
    app.config.update(kwargs)

    # In order to not partially render content of web pages,
    # the template engine must raise an exception for undefined
    # variables.
    app.jinja_options = ImmutableDict(
        undefined=jinja2.StrictUndefined, **app.jinja_options)

    # Initialize extensions.
    pages.init_app(app)

    # Register Blueprints.
    from portfolio.views import website
    app.register_blueprint(website)

    return app
