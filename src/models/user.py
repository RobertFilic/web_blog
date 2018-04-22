import uuid

from src.common.database import Database


class User(object):
    def __init__(self, email, password, _id=None):
        self. email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id # assigning an ID to the user

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
            return True
        else:
            #User exists :(
            return False


    def login(self):
        pass

    def json(self):
        pass

    def save_to_mongo(self):
        pass