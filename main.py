from router.web import app
from config.config import bcolors
from config.filesystem import makeDaemon, init
from flask_script import Command, Manager, Option
import os

manager = Manager(app)
manager.help_args = ('-?', '--help')

@manager.option('-n', '--name', help='Daemon name')
def daemon(name):
    """Daemon name"""
    makeDaemon(name)

@manager.option('-t', '--test', help='Daemon test', default=False)
def test(test):
    """Daemon name"""
    
    # all_functions = inspect.getmembers('app/Http/*', inspect.isfunction)
    # for item in all_functions:
        # print(item)


if __name__ == "__main__":
    init()
    manager.run()