from flask import session, Blueprint, jsonify, render_template, flash, redirect, url_for
from models import Subject, Admin, User,db
from auth.admin_auth import admin_req

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@admin_req
def admin():
    subjects = Subject.query.all()
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('admin/admin.html',admin=admin, subjects=subjects)

@admin_bp.route('/admin/users')
@admin_req
def user_dash_admin():
    admin = Admin.query.filter_by(email=session['email']).first()
    users = User.query.all()
    return render_template('admin/user_dash_admin.html',admin=admin, users=users)

@admin_bp.route('/admin/users/<int:user_id>/access', methods=['POST'])
@admin_req
def user_dash_admin_access(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_active = not user.is_active
        db.session.commit()
        flash('User access update successful')
    else:
        flash('User not found')
        return redirect(url_for('admin.admin'))
    return redirect(url_for('admin.user_dash_admin', user_id=user_id))

@admin_bp.route('/admin/user/<int:user_id>/view')
@admin_req
def view_user_admin(user_id):
    user = User.query.get(user_id)
    admin = Admin.query.filter_by(email=session['email']).first()

    if not user:
        flash('User not found')
        return redirect(url_for('admin.admin'))

    return render_template('admin/view_user_admin.html', user_id=user_id, user=user, admin=admin)
