import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TESTING = False
CSRF_ENABLED = True

SECRET_KEY = os.environ['SECRET_KEY']
