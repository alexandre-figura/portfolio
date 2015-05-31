#!/usr/bin/env python
import logging

from flask_script import Manager, Server

from portfolio.portfolio import app

logger = logging.getLogger(__name__)
manager = Manager(app)


if __name__ == '__main__':
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    logger.addHandler(console)
    logger.setLevel(logging.INFO)

    manager.add_command('runserver', Server(use_debugger=True))
    manager.run()
