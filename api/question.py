from flask import render_template, request, redirect, url_for, flash, session, Blueprint, jsonify
from models import db, Subject, Chapter, Quiz, Question, Admin
from auth.admin_auth import admin_req


question_bp = Blueprint('question', __name__)


@question_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/quiz/<int:quiz_id>/question/add')
@admin_req
def add_question(subject_id,chapter_id, quiz_id):
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
    return render_template('/question/add_question.html', subject=subject, chapter=chapter, quiz=quiz,admin=admin)

@question_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/quiz/<int:quiz_id>/question/add', methods=['POST'])
@admin_req
def add_question_post(subject_id, chapter_id,quiz_id):
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
    
    question_statement = request.form.get('question_statement')
    option1 = request.form.get('option1')
    option2 = request.form.get('option2')
    option3 = request.form.get('option3')
    option4 = request.form.get('option4')
    correct_option = request.form.get('correct_option')

    
    if not question_statement or not option1 or not option2 or not correct_option:
        flash('Please fill all the fields')
        return redirect(url_for('question.add_question', subject_id=subject_id, chapter_id=chapter_id, quiz_id=quiz_id))
    
    existing_question = Question.query.filter_by(quiz_id=quiz_id, question_statement=question_statement).first()
    if existing_question:
        flash('Question already exists in this Quiz!')
        return redirect(url_for('question.add_question', subject_id=subject_id, chapter_id=chapter_id, quiz_id=quiz_id))
    

    question = Question(
        question_statement=question_statement,
        option1=option1,
        option2=option2,
        option3=option3,
        option4=option4,
        correct_option=correct_option,
        quiz_id=quiz_id
    )
    db.session.add(question)
    db.session.commit()
    flash("Question Added Successfully")

    return redirect(url_for('quiz.view_quiz', subject_id=subject_id, chapter_id=chapter_id,quiz_id=quiz_id))

@question_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/quiz/<int:quiz_id>/question/<int:question_id>/delete')
@admin_req
def delete_question(subject_id, chapter_id,quiz_id, question_id):
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
    
    question = Question.query.get(question_id)
    if not quiz:
        flash('Question does not exist')
        return redirect(url_for('quiz.view_quiz', subject_id=subject_id, chapter_id=chapter_id, quiz_id=quiz_id))
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('/question/delete_question.html',subject=subject, chapter=chapter, quiz=quiz, question=question,admin=admin)

@question_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/quiz/<int:quiz_id>/question/<int:question_id>/delete', methods=['POST'])
@admin_req
def delete_question_post(subject_id,chapter_id,quiz_id,question_id):
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
    
    question = Question.query.get(question_id)
    if not quiz:
        flash('Question does not exist')
        return redirect(url_for('quiz.view_quiz', subject_id=subject_id, chapter_id=chapter_id, quiz_id=quiz_id))
    
    db.session.delete(question)
    db.session.commit()

    flash('Question Deleted Successfully')
    return redirect(url_for('quiz.view_quiz', subject_id=subject_id, chapter_id=chapter_id, quiz_id=quiz_id))

@question_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/quiz/<int:quiz_id>/question/<int:question_id>/edit')
@admin_req
def edit_question(subject_id, chapter_id, quiz_id, question_id):
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

    question = Question.query.get(question_id)
    if not question:
        flash('Question does not exist')
        return redirect(url_for('quiz.view_quiz', subject_id=subject_id, chapter_id=chapter_id, quiz_id=quiz_id))
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('/question/edit_question.html', subject=subject, chapter=chapter, quiz=quiz, question=question,admin=admin)

@question_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/quiz/<int:quiz_id>/question/<int:question_id>/edit', methods=['POST'])
@admin_req
def edit_question_post(subject_id, chapter_id, quiz_id, question_id):
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

    question = Question.query.get(question_id)
    if not question:
        flash('Question does not exist')
        return redirect(url_for('quiz.view_quiz', subject_id=subject_id, chapter_id=chapter_id, quiz_id=quiz_id))

    
    question_statement = request.form.get('question_statement')
    option1 = request.form.get('option1')
    option2 = request.form.get('option2')
    option3 = request.form.get('option3')
    option4 = request.form.get('option4')
    correct_option = request.form.get('correct_option')

    if not question_statement or not option1 or not option2 or not correct_option:
        flash('Please fill all required fields')
        return redirect(url_for('question.edit_question', subject_id=subject_id, chapter_id=chapter_id, quiz_id=quiz_id, question_id=question_id))

    question.question_statement = question_statement
    question.option1 = option1
    question.option2 = option2
    question.option3 = option3
    question.option4 = option4
    question.correct_option = correct_option

    db.session.commit()
    flash("Question Updated Successfully")

    return redirect(url_for('quiz.view_quiz', subject_id=subject_id, chapter_id=chapter_id, quiz_id=quiz_id))

@question_bp.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/quiz/<int:quiz_id>/question/<int:question_id>')
@admin_req
def view_question(subject_id, chapter_id, quiz_id, question_id):
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

    question = Question.query.get(question_id)
    if not question:
        flash('Question does not exist')
        return redirect(url_for('quiz.view_quiz', subject_id=subject_id, chapter_id=chapter_id, quiz_id=quiz_id))
    admin = Admin.query.filter_by(email=session['email']).first()
    return render_template('/question/view_question.html', subject=subject, chapter=chapter, quiz=quiz, question=question,admin=admin)

