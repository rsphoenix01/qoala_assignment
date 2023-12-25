''' THIS FILE CONTAINS THE SECURITY FUNCTIONS FOR JWT'''

from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(email, password):
    print("\n\n\n @authenticate\n\n")
    return UserModel.find_by_email(email)
        

def identity(payload):
    print("\n\n\n @identity\n\n")
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
