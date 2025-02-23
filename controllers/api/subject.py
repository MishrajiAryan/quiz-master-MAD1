from flask import render_template, request, redirect, url_for, flash, session, Blueprint, jsonify
from models import db, Subject, Admin
from datetime import datetime, timedelta
from controllers.auth.admin_auth import admin_req


subject_bp = Blueprint('subject', __name__)


@subject_bp.route('/subject/add')
@admin_req
def add_subject():
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('/subject/add_subject.html',admin=admin)

@subject_bp.route('/subject/add', methods=['POST'])
@admin_req
def add_subject_post():
    name = request.form.get('subject_name')
    description = request.form.get('subject_description')

    if not description or not name:
        flash('Please fill all the fields')
        return redirect(url_for('subject.add_subject'))
    
    existing_subject = Subject.query.filter(Subject.name == name).first()

    if existing_subject:
        flash('Subject name already exists, choose another')
        return redirect(url_for('subject.add_subject'))

    
    subject = Subject(name=name, description=description)
    db.session.add(subject)
    db.session.commit()
    flash("Subject Added Successfully")

    return redirect(url_for('admin.subject_dash_admin'))

@subject_bp.route('/subject/<int:subject_id>')
@admin_req
def view_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin.subject_dash_admin'))
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('/subject/view_subject.html',subject=subject, admin=admin)

@subject_bp.route('/subject/<int:subject_id>/edit')
@admin_req
def edit_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin.subject_dash_admin'))
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('/subject/edit_subject.html', subject=subject,admin=admin)

@subject_bp.route('/subject/<int:subject_id>/edit', methods=['POST'])
@admin_req
def edit_subject_post(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin.subject_dash_admin'))
    
    name = request.form.get('subject_name')
    description = request.form.get('subject_description')

    if not description or not name:
        flash('Please fill all the fields')
        return redirect(url_for('subject.edit_subject', subject_id=subject_id))
    
    subject.name = name
    subject.description = description

    db.session.commit()

    flash("Subject Updated Successfully")
    return redirect(url_for('admin.subject_dash_admin'))

@subject_bp.route('/subject/<int:subject_id>/delete')
@admin_req
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin.subject_dash_admin'))
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('/subject/delete_subject.html',subject=subject,admin=admin)

@subject_bp.route('/subject/<int:subject_id>/delete', methods=['POST'])
@admin_req
def delete_subject_post(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin.subject_dash_admin'))
    db.session.delete(subject)
    db.session.commit()

    flash('Subject Deleted Successfully')
    return redirect(url_for('admin.subject_dash_admin'))

