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
    category = db.Column(db.Integer, ForeignKey(Category.id))
    raise_user = db.Column(db.Integer, ForeignKey(User.id))
    raise_date = db.Column(db.DateTime)
    priority = db.Column(db.Integer)
    assign_user = db.Column(db.Integer, ForeignKey(User.id))
    open = db.Column(db.Boolean)
    notes = db.Column(db.String)
    resolution = db.Column(db.String)


    def __init__(self, title, body, category, raise_user):
        self.title = title
        self.body = body
        self.raise_user = raise_user
        self.raise_date = datetime.today()
        self.category = category
        self.priority = None
        self.assign_user = None
        self.open = True
        self.notes = None
        self.resolution = None


    def __repr__(self):
        return '<id {}>'.format(self.id)



class Settings(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    settings = db.Column(db.String)
    value = db.Column(db.Integer)


    def __init__(self, setting, value):
        self.setting = setting
        self.value = value


    def __repr__(self):
        return '<id {}>'.format(self.id)
