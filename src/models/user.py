from src.common.database import Database


class User(object):
    def __init__(self, email, password):
        self. email = email
        self.password = password

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

    #Check if user's email matches the password they sent us
    def login_valid(self):
        pass

    def register(self):
        pass

    def login(self):
        pass

    def json(self):
        pass

    def save_to_mongo(self):
        pass