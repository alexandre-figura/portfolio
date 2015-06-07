#!/usr/bin/env python

import os.path
from threading import Thread

from flask_script import Manager, Server

from portfolio import utils
from portfolio.portfolio import app

manager = Manager(app)


class RunServer(Server):
    def __call__(self, app, *args, **kwargs):
        sass_folder = os.path.join(app.root_path, 'assets', 'stylesheets')
        css_folder = os.path.join(app.static_folder, 'css')

        sass_watcher = Thread(target=utils.watch_sass_stylesheets, args=[sass_folder, css_folder], daemon=True)
        sass_watcher.start()

        super().__call__(app, *args, **kwargs)

if __name__ == '__main__':
    manager.add_command('runserver', RunServer(use_debugger=True))
    manager.run()
