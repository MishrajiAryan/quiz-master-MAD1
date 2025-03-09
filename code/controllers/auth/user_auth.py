from flask import redirect, url_for, flash, session # type: ignore
from functools import wraps

# Decorator for Authentication
def auth_req(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if session.get('email'):
            return f(*args,**kwargs)
        else:
            flash('Please login to continue')
            return redirect(url_for('auth.login'))
    return inner
