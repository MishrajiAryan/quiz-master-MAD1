from flask import render_template, request, redirect, url_for, flash, session, Blueprint, jsonify
from models import db, User, Subject, Chapter, Quiz, Question, Score
from datetime import datetime, timedelta
from auth.user_auth import auth_req


user_bp = Blueprint('user', __name__)



@user_bp.route('/user')
@auth_req
def user():
    user=User.query.filter_by(email=session['email']).first()
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()
    questions = Question.query.all()
    tomorrow = (datetime.today() + timedelta(days=1)).date()
    today = (datetime.today()).date()
    return render_template('/base/index.html', user=user, subjects=subjects, chapters=chapters,quizzes=quizzes, questions=questions, tomorrow=tomorrow,today=today)


@user_bp.route('/user/<int:user_id>/quiz/<int:quiz_id>/view')
@auth_req
def preview_quiz(user_id, quiz_id):
    user = User.query.filter_by(email=session.get('email')).first()
    if not user:
        flash('User not found')
        return redirect(url_for('user.user'))

    quiz = Quiz.query.filter_by(id=quiz_id).first()
    if not quiz:
        flash('Quiz not found')
        return redirect(url_for('user.user'))

    subject = Subject.query.all()
    chapter = Chapter.query.all()

    return render_template('user/preview_quiz.html', user=user, quiz=quiz, subject=subject, chapter=chapter, quiz_id=quiz_id, user_id=user_id)


@user_bp.route('/user/<int:user_id>/quiz/<int:quiz_id>/attempt')
@auth_req
def attempt_quiz(user_id, quiz_id):
    user = User.query.filter_by(email=session.get('email')).first()
    if not user:
        flash('User not found')
        return redirect(url_for('auth.index'))

    quiz = Quiz.query.filter_by(id=quiz_id).first()
    if not quiz:
        flash('Quiz not found')
        return redirect(url_for('auth.index'))
    
    return render_template('user/attempt_quiz.html', user=user, quiz=quiz, quiz_id=quiz_id, user_id=user_id)


@user_bp.route('/user/<int:user_id>/quiz/<int:quiz_id>/attempt', methods=['POST'])
@auth_req
def attempt_quiz_post(user_id, quiz_id):
    user = User.query.filter_by(email=session.get('email')).first()
    if not user:
        flash('User not found')
        return redirect(url_for('auth.index'))

    quiz = Quiz.query.filter_by(id=quiz_id).first()
    if not quiz:
        flash('Quiz not found')
        return redirect(url_for('auth.index'))
    
    return redirect(url_for('quiz_test', quiz_id=quiz_id, user_id=user_id))


@user_bp.route('/user/<int:user_id>/quiz/<int:quiz_id>/now')
@auth_req
def quiz_test(user_id, quiz_id):
    user = User.query.filter_by(email=session.get('email')).first()
    if not user:
        flash('User not found')
        return redirect(url_for('auth.index'))

    quiz = Quiz.query.filter_by(id=quiz_id).first()
    if not quiz:
        flash('Quiz not found')
        return redirect(url_for('auth.index'))
    
    question = quiz.questions
    
    return render_template('user/quiz_test.html', user=user, quiz=quiz,question=question, quiz_id=quiz_id, user_id=user_id)


@user_bp.route('/user/<int:user_id>/quiz/<int:quiz_id>/now', methods=['POST'])
@auth_req
def quiz_test_post(user_id, quiz_id):
    user = User.query.filter_by(email=session.get('email')).first()
    if not user:
        flash('User not found')
        return redirect(url_for('auth.index'))

    quiz = Quiz.query.filter_by(id=quiz_id).first()
    if not quiz:
        flash('Quiz not found')
        return redirect(url_for('auth.index'))
    
    questions = quiz.questions
    total_score = 0

    for question in questions:
        selected_option = request.form.get(f'question_{question.id}')
        if selected_option and int(selected_option) == question.correct_option:
            total_score = total_score +  1 

    score = Score(
        quiz_id=quiz.id,
        user_id=user.id,
        timestamp=datetime.now(),
        total_scored=total_score
    )

    db.session.add(score)
    db.session.commit()
    
    return render_template('user/quiz_result.html', user=user, quiz=quiz,question=question, quiz_id=quiz_id, user_id=user_id)



