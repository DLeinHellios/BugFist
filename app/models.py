from app import db
from datetime import datetime
from sqlalchemy import ForeignKey


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    hash = db.Column(db.String(60))
    access = db.Column(db.Integer)
    enabled = db.Column(db.Boolean)

    def __init__(self, username, email, hash, access):
        self.username = username
        self.email = email
        self.hash = hash
        self.access = access
        self.enabled = True


    def __repr__(self):
        return '<id {}>'.format(self.id)



class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    active = db.Column(db.Boolean)


    def __init__(self, name):
        self.name = name
        self.active = True


    def __repr__(self):
        return '<id {}>'.format(self.id)



class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    category_id = db.Column(db.Integer, ForeignKey(Category.id))
    category = db.relationship("Category")
    raise_user_id = db.Column(db.Integer, ForeignKey(User.id))
    raise_user = db.relationship("User", foreign_keys=raise_user_id)
    raise_date = db.Column(db.DateTime)
    priority = db.Column(db.Integer)
    open = db.Column(db.Boolean)
    resolution = db.Column(db.String)
    resolve_user_id = db.Column(db.Integer, ForeignKey(User.id))
    resolve_user = db.relationship("User", foreign_keys=resolve_user_id)
    resolve_date = db.Column(db.DateTime)


    def __init__(self, title, body, category_id, priority, raise_user_id):
        self.title = title
        self.body = body
        self.raise_user_id = raise_user_id
        self.raise_date = datetime.today()
        self.category_id = category_id
        self.priority = priority
        self.open = True


    def __repr__(self):
        return '<id {}>'.format(self.id)



class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    ticket_id = db.Column(db.Integer, ForeignKey(Ticket.id))
    ticket = db.relationship("Ticket")
    author_id = db.Column(db.Integer, ForeignKey(User.id))
    author = db.relationship("User")
    date = db.Column(db.DateTime)
    active = db.Column(db.Boolean)


    def __init__(self, body, author, ticket):
        self.body = body
        self.author = author
        self.ticket = ticket
        self.date = datetime.today()
        self.active = True


    def __repr__(self):
        return '<id {}>'.format(self.id)



class Settings(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    setting = db.Column(db.String)
    value = db.Column(db.String)


    def __init__(self, setting, value):
        self.setting = setting
        self.value = value


    def __repr__(self):
        return '<id {}>'.format(self.id)
