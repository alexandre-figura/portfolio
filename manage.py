import logging
from pathlib import Path
import re
import shutil
import sys

from flask import Response, request, url_for
from flask_script import Command, Manager, Option, Server
from selenium import webdriver
from threading import Thread

from portfolio.portfolio import app

logger = logging.getLogger(__name__)
manager = Manager(app)


class UpdateThemeAssets(Command):
    name = 'update_theme_assets'

    option_list = (
        Option('source', help="Theme's sources"),
    )

    def __init__(self):
        super().__init__()

        self.assets_updated = 0
        self.assets_theme_folder = app.config['THEME_ASSETS']
        self.assets_src_folder = None
        self.assets_dst_folder = Path(app.static_folder).absolute() / self.assets_theme_folder
        self.static_url_path = app.static_url_path

    def analyze_source_code_of_web_pages(self, views):
        assets_url = re.compile("[\"']" + self.static_url_path + "/" + self.assets_theme_folder + "/(.+?)[\"']")

        with app.test_client() as c:
            for view in views:
                response = c.get(view).data
                rendered_page = response.decode().splitlines()
                for line in rendered_page:
                    match = assets_url.search(line)
                    if match:
                        self.copy_asset(match.group(1))

    def load_web_page_in_browsers(self, views, server):
        assets_url = re.compile(app.static_url_path + "/" + self.assets_theme_folder + "/(.+)")

        @app.errorhandler(404)
        def catch_assets_not_found(error):
            if request.endpoint == 'static':
                match = assets_url.search(request.path)
                if match:
                    if self.copy_asset(match.group(1)):
                        return app.view_functions['static'](**request.view_args)
            return Response(status=404)

        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.disabled = True
        for browser in ['Firefox', 'Chrome', 'Ie']:
            try:
                browser = getattr(webdriver, browser)()
                browser.set_page_load_timeout(30)
            except Exception:
                continue  # Browser not installed
            else:
                for view in views:
                    browser.get('http://{0}:{1}{2}'.format(server[0], server[1], view))
                    browser.refresh()
            browser.close()
        werkzeug_logger.disabled = False

    def copy_asset(self, path):
        source = self.assets_src_folder / path
        destination = self.assets_dst_folder / path

        if not source.is_file():
            logger.error('The following asset does not exist: "{}"'.format(source))
            return None

        if not destination.is_file() or source.stat().st_mtime != destination.stat().st_mtime:
            try:
                if not destination.parents[0].is_dir():
                    destination.parents[0].mkdir(parents=True)
                shutil.copy2(str(source), str(destination))
            except OSError as e:
                logger.error('Unable to copy "{0}": {1}'.format(source, e))
                return None
            else:
                logger.info('Successfully copied "{0}"'.format(source))
                self.assets_updated += 1

        return destination

    def run(self, source):
        self.assets_src_folder = Path(source).absolute()

        for path in [self.assets_src_folder, self.assets_dst_folder]:
            if not path.is_dir():
                logger.critical('The following directory does not exist: "{}"'.format(path))
                sys.exit(1)

        server_params = ('localhost', 5000)
        server = Thread(target=app.run, args=server_params, daemon=True)
        server.start()

        views = [url_for(view) for view in app.view_functions if view != 'static']
        self.load_web_page_in_browsers(views, server_params)
        self.analyze_source_code_of_web_pages(views)

        if not self.assets_updated:
            logger.info("Assets are up to date!")


if __name__ == '__main__':
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    logger.addHandler(console)
    logger.setLevel(logging.INFO)

    manager.add_command('runserver', Server(use_debugger=True))
    manager.add_command(UpdateThemeAssets)
    manager.run()
