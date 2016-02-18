#!/usr/bin/env python

from pathlib import PurePath
from threading import Thread

from flask_script import Manager, Server

from portfolio.helpers import create_app
from portfolio.utils import watch_sass_stylesheets

manager = Manager(create_app())


class RunServer(Server):
    def __call__(self, app, *args, **kwargs):
        sass_folder = PurePath(app.root_path, 'stylesheets')
        css_folder = PurePath(app.static_folder, 'css')

        class SassWatcher(Thread):
            def run(self):
                try:
                    watch_sass_stylesheets(str(sass_folder), str(css_folder))
                except FileNotFoundError as e:
                    print(' * {}'.format(e))
                    print(' * Automatic reload of CSS stylesheets is deactivated')  # noqa

        SassWatcher().start()

        super().__call__(app, *args, **kwargs)

if __name__ == '__main__':
    manager.add_command('runserver', RunServer(use_debugger=True))
    manager.run()
