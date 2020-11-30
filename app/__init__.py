from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_recaptcha import ReCaptcha

# Create and config flask app
app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
recaptcha = ReCaptcha(app=app)

# Import modules
from app.models import *
from app.actions import *

# Init objects
userSession = UserSession()
userManage = UserManager()
ticketManage = TicketManager()
categoryManage = CategoryManager()

# Import views
from app.views import *
