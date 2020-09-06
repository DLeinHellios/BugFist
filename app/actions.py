from flask import session

class UserSession:
    def __init__(self):
        '''Holds methods for user actions'''
        pass


    def create_user_session(self, username, authLvl):
        session["username"] = username
        session["authLevel"] = authLvl


    def auth(self, name, passwd):
        '''Accepts user credentials, authenticates credentials, and creates builds session values'''
        #TODO build-out authentication
        if name == "user" and passwd == "pass":
            self.create_user_session(name, 0)
            return True
        elif name == "mod" and passwd == "pass":
            self.create_user_session(name, 1)
            return True
        elif name == "admin" and passwd == "pass":
            self.create_user_session(name, 2)
            return True
        else:
            return False


    def logout(self):
        if "username" in session:
            del session["username"]
            del session["authLevel"]
