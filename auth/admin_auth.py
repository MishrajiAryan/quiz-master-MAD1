from flask import redirect, url_for, flash, session
from functools import wraps
from models import Admin

# Decorator for Admin Authentication
def admin_req(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('email'):
            flash('Please login to continue')
            return redirect(url_for('auth.login'))

        admin = Admin.query.filter_by(email=session['email']).first()
        if not admin:
            flash('Access Denied')
            return redirect(url_for('auth.index'))

        return f(*args,**kwargs)
    return inner