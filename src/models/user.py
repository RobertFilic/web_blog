import uuid
from flask import session
from src.common.database import Database
from src.models.blog import Blog


class User(object):
    def __init__(self, email, password, _id=None):
        self. email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id # assigning an ID to the user = user_id
    # Filter users by email
    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("user",  {"email":email})
        if data is not None:
            return cls(**data)

    # Filter users by id/password
    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("user", {"_id": _id})
        if data is not None:
            return cls(**data)
        #return None  this part is default in Python

    @staticmethod
    #Check if user's email matches the password they sent us
    def login_valid(email, password):
        user = User.get_by_email(email) # if it finds the user in the database it will return an element, otherwise it will be None
        if user is not None:
            # Check the password
            return user.password == password # compares password from database and the one entered in the website
        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        #check if the user already exists in our database
        if user is None:
            #if user doesn't exist, we can create it
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email # we input the email into Flask session which will manage the cookies
            return True
        else:
            #User exists :(
            return False

    @staticmethod
    def login(user_email):
        session['email'] = user_email # Flask manages cookies for us. It understands when an existing user is logged and returns to the website

    @staticmethod
    def logout():
        session['email'] = None

    def get_blog(self):
        return Blog.find_by_author_id(self._id)


    def json(self):
        return {
            "email": self.email,
            "_id": self._id, # same as user_id
            "password": self.password  # not safe!!
        }


    def save_to_mongo(self):
        Database.insert("users", self.json())