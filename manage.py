# Manually manages database
import os, sys
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


from dotenv import load_dotenv
load_dotenv('.env')

from app import app, db, bcrypt
from app.models import User

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
