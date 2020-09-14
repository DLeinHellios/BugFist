import os
from flask import session
from app import db, bcrypt
from app.models import *


class UserSession:
    def create_user_session(self, userData):
        '''Creates session of authed user'''
        session["userId"] = userData.id
        session["username"] = userData.username
        session["authLevel"] = userData.access


    def auth(self, name, passwd):
        '''Accepts user credentials, authenticates credentials, and creates builds session values'''
        userData = User.query.filter_by(username=name).first()
        if userData != None and bcrypt.check_password_hash(userData.hash, passwd):
            self.create_user_session(userData)
            return True
        else:
            return False


    def logout(self):
        if "username" in session:
            del session["userId"]
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

        elif len(username) > 16:
            msg = 'Username too long: max of 16 characters'

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

        newUser = User(username, email, bcrypt.generate_password_hash(passwd).decode('utf8'), accessLevel)
        db.session.add(newUser)
        db.session.commit()



class TicketManage:
    def validate_new_ticket(self, title, body, category):
        '''Returns message to flash if ticket submission is invalid, otherwise returns blank string'''
        msg = ''
        if title == '':
            msg = 'Tickets must include a title'
        elif body == '':
            msg = 'Tickets must include a description'

        return msg


    def submit_ticket(self, title, body, category):
        '''Writes a new ticket to the database'''
        newTicket = Ticket(title, body, category, session['userId'])
        db.session.add(newTicket)
        db.session.commit()
