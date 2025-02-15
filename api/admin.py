from flask import session, Blueprint, jsonify, render_template
from models import Subject, Admin, User
from auth.admin_auth import admin_req

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@admin_req
def admin():
    subjects = Subject.query.all()
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('base/admin.html',admin=admin, subjects=subjects)

@admin_bp.route('/admin/users')
@admin_req
def user_dash_admin():
    admin = Admin.query.filter_by(email=session['email']).first()
    users = User.query.all()
    return render_template('base/user_dash_admin.html',admin=admin, users=users)
