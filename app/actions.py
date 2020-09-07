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
    def validate_new_user(self, username, email, password0, password1, registerCode):
        '''Returns a message to flash if new user submission contains errors'''
        msg = ''
        if registerCode != os.environ['REGISTER_CODE']:
            msg = 'Invalid registration code'

        elif False: # username taken
            msg = 'Username/Email already in-use'
        elif password0 != password1:
            msg = 'Passwords do not match'

        return msg



    def register_user(self, username, email, passwd):
        if User.query.all() == []:
            accessLevel = 2
        else:
            accessLevel = 0

        admin = User(username, email, bcrypt.generate_password_hash(passwd).decode('utf8'), accessLevel)
        db.session.add(admin)
        db.session.commit()
