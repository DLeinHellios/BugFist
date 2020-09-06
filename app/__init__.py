from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create and config flask app
app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

# Import modules
from app.models import *
from app.actions import *

# Init objects
user = UserSession()

# Import views
from app.views import *
