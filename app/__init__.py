from flask import Flask

# Create and config flask app
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Import modules
from app.views import *
