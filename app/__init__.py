from flask import Flask

# Create and config flask app
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Import modules
from app.users import *

# Init objects
users = Users()

# Import views
from app.views import *
