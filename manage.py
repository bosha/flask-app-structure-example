#!/usr/bin/env python
import os
from flask_script import Manager

from app import create_app

app = create_app()
app.config.from_object(os.environ['APP_SETTINGS'])
manager = Manager(app)

# Remove before make public
from flask.ext.migrate import Migrate, MigrateCommand
from app.database import db
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
