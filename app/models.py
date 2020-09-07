from app import db
from datetime import date


class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(20), unique=True)
    pw = db.Column(db.String(60))
    access = db.Column(db.Integer())
    enabled = db.Column(db.Boolean())

    def __init__(self, username, email, pw, access):
        self.username = username
        self.email = email
        self.pw = pw
        self.access = access
        self.enabled = True


    def __repr__(self):
        return '<id {}>'.format(self.id)



class Reports(db.Model):
    __tablename__ = 'Reports'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    body = db.Column(db.String())
    raiseUser = db.Column(db.Integer())
    raiseDate = db.Column(db.Date())
    priority = db.Column(db.Integer())
    assignUser = db.Column(db.Integer())
    open = db.Column(db.Boolean())


    def __init__(self, title, body, raiseUser, priority):
        self.title = title
        self.body = body
        self.raiseUser = raiseUser
        self.raiseDate = date.today()
        self.priority = priority
        assignUser = None
        open = True


    def __repr__(self):
        return '<id {}>'.format(self.id)
