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

    #When a user logs in get the user object for that respective user through using email and password
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

    #Return true if a user exists with a given email and false if there is no user
    #exists with that email, used to ensure no duplicates are in the system
    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

 #When the edit account information form is submitted by a logged in user
# take in the new values for each attribute as well as the current user id
#only change attributes that a user wants to be changed by ensuring there are no
#empty strings being passed to the edit functions
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
    
    
    #Add a new user to the system if they successfully complete the registration form
    #Checks to ensure a user with that email does not already exist
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

#Get all User attributes for the corresponding User ID
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
     
    #Return an Empty User Object to display when a User logs out
    @staticmethod
    def logout():
        return User(None)
    #Change the Password attribute of the User given the new value and the user id
    #Ensure the new password is properly hashed to protect the user when it is stored
    @staticmethod
    def changePassword(newPW, target):
        app.db.execute('''
            UPDATE Users
            SET password = :password
            WHERE id = :id
            ''', password=generate_password_hash(newPW),id=target)
        return "Success"
    #Change the email attribute of the User given the new value and the user id
    #Ensure that the new email does not exist in the User database yet
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
    #Change the first name attribute of the User given the new value and the user id
    @staticmethod
    def changeFname(newFirstName, target):
        rows = app.db.execute('''
            UPDATE Users
            SET firstname = :firstname
            WHERE id = :id
            ''', firstname=newFirstName,id=target)
    #Change the last name attribute of the User given the new value and the user id
    @staticmethod
    def changeLname(newLastName, target):
        app.db.execute('''
            UPDATE Users
            SET lastname = :lastname
            WHERE id = :id
            ''', lastname=newLastName,id=target)
#Return if the current user is the owner of a restaurant or not
    @staticmethod
    def is_owner(id):
        rows = app.db.execute("""
                                SELECT isOwner
                                FROM Users
                                WHERE id = :id
                            """,
                              id=id)
        result = rows[0][0]
        return result