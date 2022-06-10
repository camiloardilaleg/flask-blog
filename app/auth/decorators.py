from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        is_admin = getattr(current_user, 'is_admin', False)
        if not is_admin:
            abort(401)
        return func(*args, **kwargs)
    return wrapper