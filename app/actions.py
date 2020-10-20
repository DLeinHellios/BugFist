import os, datetime
from flask import session
from app import db, bcrypt
from app.models import *


class UserSession:
    def create_user_session(self, userData):
        '''Creates session of authed user'''
        session["userId"] = userData.id
        session["username"] = userData.username
        session["authLevel"] = userData.access
        session["lastPage"] = "/dashboard"


    def auth(self, name, passwd):
        '''Accepts user credentials, authenticates credentials, and creates builds session values'''
        userData = User.query.filter_by(username=name).first()
        if userData != None and bcrypt.check_password_hash(userData.hash, passwd) and userData.enabled:
            self.create_user_session(userData)
            return True
        else:
            return False


    def logout(self):
        '''Removes user data from session'''
        if "username" in session:
            del session["userId"]
            del session["username"]
            del session["authLevel"]


class UserManage:
    def __init__(self):
        '''Sets default password settings'''
        self.min_pw_length = 8
        self.max_username_length = 16

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

        elif not username.isalnum():
            msg = "Username can only contain letters and numbers"

        elif registerCode != os.environ['REGISTER_CODE']:
            msg = 'Invalid registration code'

        elif len(username) > self.max_username_length:
            msg = 'Username too long: max of 16 characters'

        elif User.query.filter_by(username=username).first() != None:
            msg = 'Username unavailable'

        elif User.query.filter_by(email=email).first() != None:
            msg = 'Email already in-use'

        else:
            msg = self.validate_password(password0, password1)

        return msg


    def register_user(self, username, email, passwd):
        '''Writes a new user to the database'''
        # Make first user admin
        if User.query.all() == []:
            accessLevel = 2
        else:
            accessLevel = 0

        # Register new user
        newUser = User(username, email, bcrypt.generate_password_hash(passwd).decode('utf8'), accessLevel)
        db.session.add(newUser)
        db.session.commit()



class TicketManage:
    def __init__(self):
        self.max_title_length = 75
        self.max_body_length = 1000
        self.max_addition_length = 600


    def validate_new_ticket(self, title, body, category):
        '''Returns message to flash if ticket submission is invalid, otherwise returns blank string'''
        msg = ''
        if title.rstrip() == '':
            msg = 'Tickets must include a title'
        elif body.rstrip() == '':
            msg = 'Tickets must include a description'
        elif len(title) > self.max_title_length:
            msg = 'Title exceeds maximum length'
        elif len(body) > self.max_body_length:
            msg = 'Description exceeds maximum length'

        return msg


    def submit_ticket(self, title, body, category, priority):
        '''Writes a new ticket to the database'''
        newTicket = Ticket(title.rstrip(), body.rstrip(), category, priority, session['userId'])
        db.session.add(newTicket)
        db.session.commit()


    def validate_ticket_addition(self, addition):
        '''Returns a message to flash if resolution or note is invalid, otherwise returns blank string'''
        msg = ''
        if addition.rstrip() == "":
            msg = 'Please enter a resolution'
        elif len(addition) > self.max_addition_length:
            msg = 'Resolution exceeds maximum length'

        return msg


    def resolve_ticket(self, id, resolution):
        '''Adds resolution data to an existing ticket'''
        ticket = Ticket.query.filter_by(id=id).first()
        ticket.resolution = resolution.rstrip()
        ticket.resolve_user_id = session['userId']
        ticket.resolve_date = datetime.today()
        ticket.open = False
        db.session.commit()


    def add_note(self, ticketId, note):
        '''Create a new ticket note in database'''
        newNote = Note(note.rstrip(), session['userId'], ticketId)
        db.session.add(newNote)
        db.session.commit()


    def get_dashboard_data(self, tickets):
        '''Computes and returns values for charts on dashboard'''
        data = {
            "ticket_status": {"open":0, "closed":0},
            "open_priority": {"low": 0, "med": 0, "high": 0, "na":0},
            "category_counts": {"N/A": 0}}

        for ticket in tickets:

            # Status
            if ticket.open:
                data['ticket_status']['open'] += 1

                # Priority
                if ticket.priority == 3:
                    data['open_priority']['low'] += 1
                elif ticket.priority == 2:
                    data['open_priority']['med'] += 1
                elif ticket.priority == 1:
                    data['open_priority']['high'] += 1
                else:
                    data['open_priority']['na'] += 1

            else:
                data['ticket_status']['closed'] += 1

            # Category
            if ticket.category == None:
                data['category_counts']['N/A'] += 1

            else:
                if ticket.category.name in data['category_counts']:
                    data['category_counts'][ticket.category.name] += 1
                else:
                    data['category_counts'][ticket.category.name] = 1


        data['top_categories'] = [(name, count) for name, count in sorted(data['category_counts'].items())]

        # Pad for bar chart
        while len(data['top_categories']) < 3:
            data['top_categories'] += [('',0)]

        return data
