#!/usr/bin/env python

import os.path
import threading

from flask_script import Manager, Server

from portfolio import helpers, utils

manager = Manager(helpers.create_app())


class RunServer(Server):
    def __call__(self, app, *args, **kwargs):
        sass_folder = os.path.join(app.root_path, 'assets', 'stylesheets')
        css_folder = os.path.join(app.static_folder, 'css')

        class SassWatcher(threading.Thread):
            def run(self):
                try:
                    utils.watch_sass_stylesheets(sass_folder, css_folder)
                except FileNotFoundError as e:
                    print(' * {}'.format(e))
                    print(' * Automatic reload of CSS stylesheets is deactivated')  # noqa

        SassWatcher().start()

        super().__call__(app, *args, **kwargs)

if __name__ == '__main__':
    manager.add_command('runserver', RunServer(use_debugger=True))
    manager.run()
