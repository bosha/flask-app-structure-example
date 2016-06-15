#!/usr/bin/env python
import os
from flask_script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import create_app
from app.database import db

app = create_app()
app.config.from_object(os.environ['APP_SETTINGS'])
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
