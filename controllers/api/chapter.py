from flask import render_template, request, redirect, url_for, flash, session, Blueprint, jsonify
from models import db, Subject, Chapter, Admin, Quiz
from datetime import datetime
from functools import wraps
from controllers.auth.admin_auth import admin_req

chapter_bp = Blueprint('chapter', __name__)


@chapter_bp.route('/subject/<int:subject_id>/chapter/add')
@admin_req
def add_chapter(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject does not exist')
        return redirect(url_for('admin.subject_dash_admin'))
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('/chapter/add_chapter.html', subject=subject,admin=admin)


@chapter_bp.route('/subject/<int:subject_id>/chapter/add', methods=['POST'])
@admin_req
def add_chapter_post(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject does not exist')
        return redirect(url_for('admin.subject_dash_admin'))
    
    name = request.form.get('chapter_name')
    description = request.form.get('chapter_description')
    
    if not description or not name:
        flash('Please fill all the fields')
        return redirect(url_for('chapter.add_chapter', subject_id=subject_id))
    
    existing_chapter = Chapter.query.filter_by(subject_id=subject_id, name=name).first()
    if existing_chapter:
        flash('Chapter name already exists for this subject!')
        return redirect(url_for('chapter.add_chapter', subject_id=subject_id))
    
    chapter = Chapter(name=name, description=description, subject_id=subject_id)
    db.session.add(chapter)
    db.session.commit()
    flash("Chapter Added Successfully")

    return redirect(url_for('subject.view_subject', subject_id=subject_id))

@chapter_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/delete')
@admin_req
def delete_chapter(subject_id, chapter_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject does not exist')
        return redirect(url_for('admin.subject_dash_admin'))
    
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('subject.view_subject', subject_id=subject_id))
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('/chapter/delete_chapter.html',subject=subject, chapter=chapter,admin=admin)


@chapter_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/delete', methods=['POST'])
@admin_req
def delete_chapter_post(subject_id,chapter_id):
    subject = Subject.query.get(subject_id)
    
    if not subject:
        flash('Subject does not exist')
        return redirect(url_for('admin.subject_dash_admin'))
    
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('subject.view_subject', subject_id=subject_id))
    
    db.session.delete(chapter)
    db.session.commit()

    flash('Chapter Deleted Successfully')
    return redirect(url_for('subject.view_subject', subject_id=subject_id))


@chapter_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/edit')
@admin_req
def edit_chapter(subject_id,chapter_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin.subject_dash_admin'))

    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('subject.view_subject', subject_id=subject_id))
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('/chapter/edit_chapter.html', subject=subject, chapter=chapter,admin=admin)

@chapter_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/edit', methods=['POST'])
@admin_req
def edit_chapter_post(subject_id,chapter_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin.subject_dash_admin'))
    
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('subject.view_subject', subject_id=subject_id))
    
    name = request.form.get('chapter_name')
    description = request.form.get('chapter_description')

    if not description or not name:
        flash('Please fill all the fields')
        return redirect(url_for('chapter.edit_chapter',subject_id=subject_id, chapter_id=chapter_id))
    
    chapter.name = name
    chapter.description = description

    db.session.commit()

    flash("Chapter Updated Successfully")
    return redirect(url_for('subject.view_subject', subject_id=subject_id))

@chapter_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>')
@admin_req
def view_chapter(subject_id,chapter_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin.subject_dash_admin'))
    
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('subject.view_subject', subject_id=subject_id))
    admin = Admin.query.filter_by(email=session['email']).first()

    query = request.args.get('query', '').strip()

    # Fetch all quizzes for the given chapter
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id)

    if query:
        quizzes = quizzes.filter(Quiz.name.ilike(f"%{query}%"))

    quizzes = quizzes.all()

    return render_template('/chapter/view_chapter.html',subject=subject, chapter=chapter,admin=admin, quizzes=quizzes)
