from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, isOwner, restaurantOwned):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.isOwner = isOwner
        self.restaurantOwned = restaurantOwned

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, isOwner, restaurantOwned
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def edit(email, pw, fname, lname, id):
        if(not(pw == "")):
            User.changePassword(pw, id)
        if(not(lname == "")):
            User.changeLname(lname, id)
        if(not(fname == "")):
            User.changeFname(fname, id)
        if (not (email == "")):
            User.changeEmail(email,id)
        return "Success, user information updated"
    @staticmethod
    def register(email, password, firstname, lastname):
        boo = User.email_exists(email)
        if not boo:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, isOwner, restaurantOwned)
VALUES(:email, :password, :firstname, :lastname, :isOwner, :restaurantOwned)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname, isOwner = False, restaurantOwned = 0)
            id = rows[0][0]
            return "Success, user registered"
        else:
            return "Email in use, please use a differnt email and re-register"


    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, isOwner, restaurantOwned
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None
     
    
    @staticmethod
    def logout():
        return User(None)
    
    @staticmethod
    def changePassword(newPW, target):
        app.db.execute('''
            UPDATE Users
            SET password = :password
            WHERE id = :id
            ''', password=generate_password_hash(newPW),id=target)
        return "Success"
    @staticmethod
    def changeEmail(newEmail, target):
        boo = User.email_exists(newEmail)
        if boo:
            return "Email already exists in the system, please choose another"
        app.db.execute('''
            UPDATE Users
            SET email = :email
            WHERE id = :id
            ''', password=newEmail,id=target)
        return "Success"
    @staticmethod
    def changeFname(newFirstName, target):
        rows = app.db.execute('''
            UPDATE Users
            SET firstname = :firstname
            WHERE id = :id
            ''', firstname=newFirstName,id=target)
    def changeLname(newLastName, target):
        app.db.execute('''
            UPDATE Users
            SET lastname = :lastname
            WHERE id = :id
            ''', lastname=newLastName,id=target)
