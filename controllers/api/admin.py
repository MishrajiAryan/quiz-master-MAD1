from flask import session, Blueprint, jsonify, render_template, flash, redirect, url_for, request
from models import Subject, Admin, User,db, Score, Quiz
from controllers.auth.admin_auth import admin_req

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@admin_req
def admin():
    subjects = Subject.query.all()
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('admin/admin.html',admin=admin, subjects=subjects)

@admin_bp.route('/admin/subjects')
@admin_req
def subject_dash_admin():
    query = request.args.get('query', '').strip()  # Get the search query
    admin = Admin.query.filter_by(email=session['email']).first()

    if query:
        subjects = Subject.query.filter(Subject.name.ilike(f"%{query}%")).all()
    else:
        subjects = Subject.query.all()

    return render_template('admin/subject_dash_admin.html',admin=admin, subjects=subjects)

@admin_bp.route('/admin/users')
@admin_req
def user_dash_admin():
    admin = Admin.query.filter_by(email=session['email']).first()

    filter_by = request.args.get('filter', 'id')  # Default filter is 'id'
    query = request.args.get('query', '').strip()

    # Base query
    users = User.query

    if query:
        if filter_by == "id":
            users = users.filter(User.id == query)
        elif filter_by == "name":
            users = users.filter(User.name.ilike(f"%{query}%"))  # Case-insensitive search
        elif filter_by == "email":
            users = users.filter(User.email.ilike(f"%{query}%"))
        elif filter_by == "phone":
            users = users.filter(User.phone_number.ilike(f"%{query}%"))

    users = users.all()

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
    score = Score.query.filter_by(user_id=user_id).all()

    if not user:
        flash('User not found')
        return redirect(url_for('admin.admin'))

    filter_by = request.args.get('filter', 'id')  # Default filter is 'id'
    query = request.args.get('query', '').strip()

    # Base query
    score_query = Score.query.filter_by(user_id=user_id)

    if query:
        if filter_by == "id":
            score_query = score_query.filter(Score.quiz_id == query)
        elif filter_by == "name":
            score_query = score_query.join(Quiz).filter(Quiz.name.ilike(f"%{query}%"))  # Case-insensitive search

    score = score_query.all()

    
    return render_template('admin/view_user_admin.html', user_id=user_id, user=user, admin=admin, score=score)


@admin_bp.route('/admin/summary')
@admin_req
def admin_summary():
    subjects = Subject.query.all()
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('admin/admin_summary.html',admin=admin, subjects=subjects)

