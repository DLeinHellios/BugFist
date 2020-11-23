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

        # Update Last Login
        user = User.query.filter_by(id=userData.id).first()
        user.last_login = datetime.today()
        db.session.commit()


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
            del session["lastPage"]



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


    def get_user_data(self, users):
        '''Returns user data for admin config charts'''
        data = {
            "role_counts": [0,0,0]} # Count roles by access level - 0,1,2
        resolve_counter = {}
        submit_counter = {}

        for user in users:
            if user.enabled: # Filter disabled users from charts
                data['role_counts'][user.access] += 1
                submit_counter[user.username] = len(user.submissions)

                if user.access > 0: # Filter standard users from resolve counts
                    resolve_counter[user.username] = len(user.resolutions)

        data['resolve_counts'] = sorted(resolve_counter.items(), key=lambda x:x[1], reverse=True)
        data['submit_counts'] = sorted(submit_counter.items(), key=lambda x:x[1], reverse=True)

        # Pad for bar chart
        while len(data['resolve_counts']) < 3:
            data['resolve_counts'] += [('',0)]

        while len(data['submit_counts']) < 3:
            data['submit_counts'] += [('',0)]

        return data


    def edit_permissions(self, id, access, enabled):
        user = User.query.filter_by(id=id).first()

        # Validate access
        if access == "0":
            user.access = 0
        elif access == "1":
            user.access = 1
        elif access == "2":
            user.access = 2
        else:
            user.access = 0

        # Convert "on" string from form
        user.enabled = False
        if enabled:
            user.enabled = True

        db.session.commit()



class TicketManage:
    def __init__(self):
        self.max_title_length = 75
        self.max_body_length = 1000
        self.max_addition_length = 600 # For notes and resolution text


    def validate_new_ticket(self, title, body, category):
        '''Returns message to flash if ticket submission is invalid, otherwise returns blank string'''
        msg = ''
        if title.strip() == '':
            msg = 'Tickets must include a title'
        elif body.strip() == '':
            msg = 'Tickets must include a description'
        elif len(title) > self.max_title_length:
            msg = 'Title exceeds maximum length'
        elif len(body) > self.max_body_length:
            msg = 'Description exceeds maximum length'

        return msg


    def submit_ticket(self, title, body, category, priority):
        '''Writes a new ticket to the database'''

        # Handle missing values
        if category == '0':
            category = None
        if priority == '0':
            priority = None

        newTicket = Ticket(title.strip(), body.strip(), category, priority, session['userId'])
        db.session.add(newTicket)
        db.session.commit()


    def validate_ticket_addition(self, addition):
        '''Returns a message to flash if resolution or note is invalid, otherwise returns blank string'''
        msg = ''
        if addition.strip() == "":
            msg = 'Please enter a resolution'
        elif len(addition) > self.max_addition_length:
            msg = 'Resolution exceeds maximum length'

        return msg


    def resolve_ticket(self, id, resolution):
        '''Adds resolution data to an existing ticket'''
        ticket = Ticket.query.filter_by(id=id).first()
        ticket.resolution = resolution.strip()
        ticket.resolve_user_id = session['userId']
        ticket.resolve_date = datetime.today()
        ticket.open = False
        db.session.commit()


    def add_note(self, ticketId, note):
        '''Create a new ticket note in database'''
        newNote = Note(note.strip(), session['userId'], ticketId)
        db.session.add(newNote)
        db.session.commit()


    def get_dashboard_data(self, tickets):
        '''Computes and returns values for charts on dashboard'''
        data = {
            "ticket_status": {"open":0, "closed":0},
            "open_priority": {"low": 0, "med": 0, "high": 0, "na":0}}

        category_counts = {'Uncategorized': 0}

        for ticket in tickets:

            # Open tickets
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

                # Category
                if ticket.category == None:
                    category_counts['Uncategorized'] += 1

                else:
                    if ticket.category.name in category_counts:
                        category_counts[ticket.category.name] += 1
                    else:
                        category_counts[ticket.category.name] = 1

            # Closed tickets
            else:
                data['ticket_status']['closed'] += 1

        data['top_categories'] = sorted(category_counts.items(), key=lambda x:x[1], reverse=True)

        # Pad for bar chart
        while len(data['top_categories']) < 3:
            data['top_categories'] += [('',0)]

        return data



class CategoryManage:
    def add(self, name, description, active):
        '''Adds a new category'''
        # Convert "on" string from form
        isActive = False
        if active:
            isActive = True

        newCat = Category(name, description, isActive)
        db.session.add(newCat)
        db.session.commit()
