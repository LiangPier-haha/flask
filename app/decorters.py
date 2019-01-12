from functools import wraps
from flask import abort
from .models import Permission
from flask_login import current_user

def fun(permission):
    def fun1(f):

        @wraps(f)
        def fun2(*args,**keyargs):
            if current_user.can(permission):
                abort(403)
            return f(*args,**keyargs)
        return fun2
    return fun1

def admin_required(f):
    return fun(Permission.ADMIN)(f)

