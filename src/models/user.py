import datetime
import uuid
from flask import session
from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id  # assigning an ID to the user = user_id

    # FILTER USERS BY EMAIL
    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("user", {"email": email})
        if data is not None:
            return cls(**data)

    # FITLER USERS BY ID/PASSOWRD
    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("user", {"_id": _id})
        if data is not None:
            return cls(**data)
        # return None  this part is default in Python

    #VALIDATING USER'S ACCOUNT
    @staticmethod
    # Check if user's email matches the password they sent us
    def login_valid(email, password):
        user = User.get_by_email(
            email)  # if it finds the user in the database it will return an element, otherwise it will be None
        if user is not None:
            # Check the password
            return user.password == password  # compares password from database and the one entered in the website
        return False

    # REGISTER USER
    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        # check if the user already exists in our database
        if user is None:
            # if user doesn't exist, we can create it
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email  # we input the email into Flask session which will manage the cookies
            return True
        else:
            # User exists :(
            return False
    # LOGIN
    @staticmethod
    def login(user_email):
        session[
            'email'] = user_email  # Flask manages cookies for us. It understands when an existing user is logged and returns to the website

    # LOGOUT
    @staticmethod
    def logout():
        session['email'] = None

    # SEARCH USER'S BLOG
    def get_blog(self):
        return Blog.find_by_author_id(self._id)

    # WRITE A NEW BLOG
    def new_blog(self, title, description):
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)

        blog.save_to_mongo()

    # WRITE A NEW POST
    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        blog = Blog.from_mongo(blog_id) # user could have multiple blogs, therefore we have to select the right one
        blog.new_post(title=title,
                      content=content,
                      date=date)

    # CREATE A JSON FILE
    def json(self):
        return {
            "email": self.email,
            "_id": self._id,  # same as user_id
            "password": self.password  # not safe!!
        }

    # SAVE TO DATABASE
    def save_to_mongo(self):
        Database.insert("users", self.json())
