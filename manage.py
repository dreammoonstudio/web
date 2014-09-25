#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

import os
from app import create_app, db
#from app.models import User, Role
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

"""
Which config mode do you want?
valid options: 'development'|'production'|'test'
"""
config_name = os.environ.get("DM_CONFIG") or "default"

app = create_app(config_name)
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()

    