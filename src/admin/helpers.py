from functools import wraps
from polls.models import User
from flask_login import current_user
from flask import make_response

current_user: User

def superuser_only(function):
    
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.is_anonymous:
            return make_response('Unauthorized', 401)
        if not current_user.is_superuser:
            return make_response('Forbidden', 403)
        return function(*args, **kwargs)
    return wrapper