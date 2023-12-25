from db import mongo
import json


class UserModel:
    def __init__(self, _id, google_id, username, email, picture):
        self._id = None
        if _id:
            self._id = str(_id)
        self.google_id = google_id
        self.username = username
        self.email = email
        self.picture = picture

    def json(self, with_id=True):
        json_object = {
            "google_id": self.google_id,
            "username": self.username,
            "email": self.email,
            "picture": self.picture
        }
        if with_id:
            json_object["_id"] = self._id

        return json_object

    def save_to_db(self):
        saved = mongo.db.users.insert(self.json(False))
        return

    def delete_from_db(self):
        pass

    @classmethod
    def find_by_username(cls, username):
        return cls.find_one("username", username)

    @classmethod
    def find_by_id(cls, _id):
        return cls.find_one("_id", _id)

    @classmethod
    def find_by_email(cls, email):
        return cls.find_one("email", email)

    @classmethod
    def find_one(cls, selector, value):
        user = mongo.db.users.find_one({selector: value})

        if user:
            return UserModel(**user)

        return user
