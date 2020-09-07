from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Create and config flask app
app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Import modules
from app.models import *
from app.actions import *

# Init objects
userSession = UserSession()
userManage = UserManage()

# Import views
from app.views import *
