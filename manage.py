#!/usr/bin/env python
from flask_script import Manager, Server

from portfolio import helpers
from portfolio.portfolio import app

manager = Manager(app)


class RunServer(Server):
    def __call__(self, app, *args, **kwargs):
        helpers.auto_reload_css(app, 'assets/stylesheets', 'css')
        super().__call__(app, *args, **kwargs)

if __name__ == '__main__':
    manager.add_command('runserver', RunServer(use_debugger=True))
    manager.run()
