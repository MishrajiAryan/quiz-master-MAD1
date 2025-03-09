from flask import render_template, request, redirect, url_for, flash, session, Blueprint, jsonify
from models import db, Subject, Chapter, Quiz, Admin, Question
from datetime import datetime
from controllers.auth.admin_auth import admin_req

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/quiz/add')
@admin_req
def add_quiz(subject_id,chapter_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject does not exist')
        return redirect(url_for('admin.subject_dash_admin'))
    
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('subject.view_subject', subject_id=subject_id))
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('/quiz/add_quiz.html', subject=subject, chapter=chapter,admin=admin)

@quiz_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/quiz/add', methods=['POST'])
@admin_req
def add_quiz_post(subject_id, chapter_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject does not exist')
        return redirect(url_for('admin.subject_dash_admin'))
    
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('subject.view_subject', subject_id=subject_id))
    
    name = request.form.get('quiz_name')
    date_of_quiz = request.form.get('date_of_quiz')
    time_duration = request.form.get('time_duration')
    remarks = request.form.get('remarks')

    if time_duration =='00:00':
        flash('Time duration cannot be zero')
        return redirect(url_for('quiz.add_quiz', subject_id=subject_id, chapter_id=chapter_id))

    
    if not name or not date_of_quiz or not time_duration or not remarks:
        flash('Please fill all the fields')
        return redirect(url_for('quiz.add_quiz', subject_id=subject_id, chapter_id=chapter_id))
    
    existing_quiz = Quiz.query.filter_by(chapter_id=chapter_id, name=name).first()
    if existing_quiz:
        flash('Quiz name already exists for this chapter!')
        return redirect(url_for('quiz.add_quiz', subject_id=subject_id, chapter_id=chapter_id))
    
    date_of_quiz = datetime.strptime(date_of_quiz, "%Y-%m-%d").date()

    quiz = Quiz(name=name, date_of_quiz=date_of_quiz,remarks=remarks, 
                time_duration=time_duration , chapter_id=chapter_id)
    db.session.add(quiz)
    db.session.commit()
    flash("Quiz Added Successfully")

    return redirect(url_for('chapter.view_chapter', subject_id=subject_id, chapter_id=chapter_id))

@quiz_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/quiz/<int:quiz_id>/delete')
@admin_req
def delete_quiz(subject_id, chapter_id,quiz_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject does not exist')
        return redirect(url_for('admin.subject_dash_admin'))
    
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('subject.view_subject', subject_id=subject_id))
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash('Quiz does not exist')
        return redirect(url_for('chapter.view_chapter', subject_id=subject_id, chapter_id=chapter_id))
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('/quiz/delete_quiz.html',subject=subject, chapter=chapter, quiz=quiz,admin=admin)

@quiz_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/quiz/<int:quiz_id>/delete', methods=['POST'])
@admin_req
def delete_quiz_post(subject_id,chapter_id,quiz_id):
    subject = Subject.query.get(subject_id)
    
    if not subject:
        flash('Subject does not exist')
        return redirect(url_for('admin.subject_dash_admin'))
    
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('subject.view_subject', subject_id=subject_id))
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash('Quiz does not exist')
        return redirect(url_for('chapter.view_chapter', subject_id=subject_id, chapter_id=chapter_id))
    
    db.session.delete(quiz)
    db.session.commit()

    flash('Quiz Deleted Successfully')
    return redirect(url_for('chapter.view_chapter', subject_id=subject_id, chapter_id=chapter_id))

@quiz_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/quiz/<int:quiz_id>/edit')
@admin_req
def edit_quiz(subject_id,chapter_id,quiz_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin.subject_dash_admin'))

    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('subject.view_subject', subject_id=subject_id))
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash('Quiz does not exist')
        return redirect(url_for('chapter.view_chapter', subject_id=subject_id, chapter_id=chapter_id))
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('/quiz/edit_quiz.html', subject=subject, chapter=chapter, quiz=quiz,admin=admin)

@quiz_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/quiz/<int:quiz_id>/edit', methods=['POST'])
@admin_req
def edit_quiz_post(subject_id,chapter_id, quiz_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin.subject_dash_admin'))
    
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('subject.view_subject', subject_id=subject_id))
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash('Quiz does not exist')
        return redirect(url_for('chapter.view_chapter', subject_id=subject_id, chapter_id=chapter_id))
    
    name = request.form.get('quiz_name')
    date_of_quiz = request.form.get('date_of_quiz')
    time_duration = request.form.get('time_duration')
    remarks = request.form.get('remarks')

    if time_duration =='00:00':
        flash('Time duration cannot be zero')
        return redirect(url_for('quiz.add_quiz', subject_id=subject_id, chapter_id=chapter_id))
    
    if not name or not date_of_quiz or not time_duration or not remarks:
        flash('Please fill all the fields')
        return redirect(url_for('quiz.add_quiz', subject_id=subject_id, chapter_id=chapter_id))
    
    date_of_quiz = datetime.strptime(date_of_quiz, "%Y-%m-%d").date()

    quiz.name=name
    quiz.date_of_quiz=date_of_quiz
    quiz.remarks=remarks 
    quiz.time_duration=time_duration
    
    db.session.commit()

    flash("Quiz Updated Successfully")
    return redirect(url_for('chapter.view_chapter', subject_id=subject_id, chapter_id=chapter_id))

@quiz_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/quiz/<int:quiz_id>')
@admin_req
def view_quiz(subject_id,chapter_id,quiz_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin.subject_dash_admin'))
    
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('subject.view_subject', subject_id=subject_id))
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash('Quiz does not exist')
        return redirect(url_for('chapter.view_chapter', subject_id=subject_id, chapter_id=chapter_id))
    # Retrieve search query
    query = request.args.get('query', '').strip()

    # Get all questions related to the quiz
    questions = Question.query.filter_by(quiz_id=quiz_id)

    # If search query is provided, filter questions by statement
    if query:
        questions = questions.filter(Question.question_statement.ilike(f"%{query}%"))

    # Execute the query
    questions = questions.all()

    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('/quiz/view_quiz.html', subject=subject, chapter=chapter, quiz=quiz, questions=questions, admin=admin)
