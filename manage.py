#!/usr/bin/env python
import logging

from flask_script import Manager, Server

from portfolio import helpers
from portfolio.portfolio import app

logger = logging.getLogger(__name__)
manager = Manager(app)


class RunServer(Server):
    def __call__(self, app, *args, **kwargs):
        helpers.auto_reload_css(app, 'assets/stylesheets', 'css')
        super().__call__(app, *args, **kwargs)

if __name__ == '__main__':
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    logger.addHandler(console)
    logger.setLevel(logging.INFO)

    manager.add_command('runserver', RunServer(use_debugger=True))
    manager.run()
