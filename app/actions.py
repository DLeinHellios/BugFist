import os
from flask import session
from app import db, bcrypt
from app.models import User


class UserSession:
    def create_user_session(self, username, authLvl):
        '''Creates session of authed user'''
        session["username"] = username
        session["authLevel"] = authLvl


    def auth(self, name, passwd):
        '''Accepts user credentials, authenticates credentials, and creates builds session values'''
        #TODO build-out authentication
        userData = User.query.filter_by(username=name).first()
        if userData != None and bcrypt.check_password_hash(userData.pw, passwd):
            # Pull user values from db
            self.create_user_session(name, userData.access)
            return True
        else:
            return False


    def logout(self):
        if "username" in session:
            del session["username"]
            del session["authLevel"]



class UserManage:
    def __init__(self):
        self.min_pw_length = 8


    def validate_password(self, password0, password1):
        '''Returns a message to flash if password fails validation, otherwise returns blank string'''
        msg = ''
        if password0 != password1:
            msg = 'Passwords do not match, please try again'

        elif len(password0) < self.min_pw_length:
            msg = 'Password not long enough, minimum of {} characters'.format(self.min_pw_length)

        return msg


    def validate_new_user(self, username, email, password0, password1, registerCode):
        '''Returns a message to flash if new user submission contains errors, returns blank string if valid'''
        msg = ''

        if '' in [username, email, password0, password1, registerCode]:
            msg = "Please complete all items to continue"

        elif registerCode != os.environ['REGISTER_CODE']:
            msg = 'Invalid registration code'

        elif User.query.filter_by(username=username).first() != None:
            msg = 'Username unavailable'

        elif User.query.filter_by(email=email).first() != None:
            msg = 'Email already in-use'

        else:
            msg = self.validate_password(password0, password1)

        return msg



    def register_user(self, username, email, passwd):
        '''Writes new user to db, first user will be created as admin'''
        if User.query.all() == []:
            accessLevel = 2
        else:
            accessLevel = 0

        admin = User(username, email, bcrypt.generate_password_hash(passwd).decode('utf8'), accessLevel)
        db.session.add(admin)
        db.session.commit()
