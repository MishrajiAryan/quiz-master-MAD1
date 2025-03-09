from flask import render_template, request, redirect, url_for, flash, session, Blueprint, jsonify # type: ignore
from models import db, User, Subject, Chapter, Quiz, Question, Score, Admin
from datetime import datetime, timedelta
from controllers.auth.user_auth import auth_req


user_bp = Blueprint('user', __name__)



@user_bp.route('/user')
@auth_req
def user():
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        flash('Admin in session, cannot access')
        return redirect(url_for('admin.admin'))
    
    user=User.query.filter_by(email=session['email']).first()
    score = Score.query.filter_by(user_id=user.id).all()

    has_attempted = {score.quiz_id for score in score} #creating a set to list all quiz id attempted by user

    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()
    questions = Question.query.all()
    tomorrow = (datetime.today() + timedelta(days=1)).date()
    today = (datetime.today()).date()

    return render_template('/base/index.html',has_attempted=has_attempted, user=user, subjects=subjects,score=score, chapters=chapters,quizzes=quizzes, questions=questions, tomorrow=tomorrow,today=today)



@user_bp.route('/user/<int:user_id>/quiz/<int:quiz_id>/view')
@auth_req
def preview_quiz(user_id, quiz_id):

    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        flash('Admin in session, cannot access')
        return redirect(url_for('admin.admin'))

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
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        flash('Admin in session, cannot access')
        return redirect(url_for('admin.admin'))
    
    user = User.query.filter_by(email=session.get('email')).first()
    if not user:
        flash('User not found')
        return redirect(url_for('auth.index'))

    quiz = Quiz.query.filter_by(id=quiz_id).first()
    if not quiz:
        flash('Quiz not found')
        return redirect(url_for('auth.index'))
    
    score = Score.query.filter_by(user_id=user.id).all()
    has_attempted = {score.quiz_id for score in score} #creating a set to list all quiz id attempted by user
    if quiz.id in has_attempted:
        flash('Quiz already attempted.')
        return redirect(url_for('auth.index'))

    return render_template('user/attempt_quiz.html', user=user, quiz=quiz, quiz_id=quiz_id, user_id=user_id)


@user_bp.route('/user/<int:user_id>/quiz/<int:quiz_id>/attempt', methods=['POST'])
@auth_req
def attempt_quiz_post(user_id, quiz_id):
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        flash('Admin in session, cannot access')
        return redirect(url_for('admin.admin'))
    
    user = User.query.filter_by(email=session.get('email')).first()
    if not user:
        flash('User not found')
        return redirect(url_for('auth.index'))

    quiz = Quiz.query.filter_by(id=quiz_id).first()
    if not quiz:
        flash('Quiz not found')
        return redirect(url_for('auth.index'))
    
    
    return redirect(url_for('user.quiz_test', quiz_id=quiz_id, user_id=user_id))


@user_bp.route('/user/<int:user_id>/quiz/<int:quiz_id>/now')
@auth_req
def quiz_test(user_id, quiz_id):
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        flash('Admin in session, cannot access')
        return redirect(url_for('admin.admin'))
    
    user = User.query.filter_by(email=session.get('email')).first()
    if not user:
        flash('User not found')
        return redirect(url_for('auth.index'))

    quiz = Quiz.query.filter_by(id=quiz_id).first()
    if not quiz:
        flash('Quiz not found')
        return redirect(url_for('auth.index'))
    
    question = quiz.questions

    score = Score.query.filter_by(user_id=user.id).all()

    has_attempted = {score.quiz_id for score in score} #creating a set to list all quiz id attempted by user
    if quiz.id in has_attempted:
        flash('Quiz already attempted.')
        return redirect(url_for('auth.index'))
    
    return render_template('user/quiz_test.html', user=user, quiz=quiz,question=question, quiz_id=quiz_id, user_id=user_id)


@user_bp.route('/user/<int:user_id>/quiz/<int:quiz_id>/now', methods=['POST'])
@auth_req
def quiz_test_post(user_id, quiz_id):
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        flash('Admin in session, cannot access')
        return redirect(url_for('admin.admin'))
    
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
    total_questions = len(questions)

    for question in questions:
        selected_option = request.form.get(f'question_{question.id}')
        if selected_option and int(selected_option) == question.correct_option:
            total_score = total_score +  1 

    percentage_score = 100*(total_score/total_questions)

    score = Score(
        quiz_id=quiz.id,
        user_id=user.id,
        timestamp=datetime.now(),
        total_score =total_score,
        total_questions = total_questions,
        percentage_score = "{:.2f}".format(percentage_score),
    )

    db.session.add(score)
    db.session.commit()
   
    return redirect(url_for('user.quiz_result', user_id=user.id, quiz_id=quiz.id))


@user_bp.route('/user/<int:user_id>/quiz/attempted')
@auth_req
def past_quiz_attempt(user_id):
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        flash('Admin in session, cannot access')
        return redirect(url_for('admin.admin'))
    
    user = User.query.filter_by(email=session.get('email')).first()
    if not user:
        flash('User not found')
        return redirect(url_for('auth.index'))

    query = request.args.get('query', '').strip()

    # Fetch past quiz attempts, filter by quiz name if a search query is provided
    score = Score.query.filter_by(user_id=user_id)
    
    if query:
        score = score.join(Quiz).filter(Quiz.name.ilike(f"%{query}%"))

    score = score.all()
    
    return render_template('user/past_quiz_attempt.html', user=user,score=score, user_id=user_id)


@user_bp.route('/user/<int:user_id>/quiz/<int:quiz_id>/result')
@auth_req
def quiz_result(user_id, quiz_id):
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        flash('Admin in session, cannot access')
        return redirect(url_for('admin.admin'))
    
    user = User.query.filter_by(email=session.get('email')).first()
    if not user:
        flash('User not found')
        return redirect(url_for('auth.index'))
    
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    if not quiz:
        flash('Quiz not found')
        return redirect(url_for('auth.index'))
    
    score = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()


    return render_template('user/quiz_result.html', user=user,score=score, quiz=quiz, user_id=user_id)


@user_bp.route('/user/<int:user_id>/summary')
@auth_req
def user_summary(user_id):
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        flash('Admin in session, cannot access')
        return redirect(url_for('admin.admin'))
    
    user = User.query.filter_by(email=session.get('email')).first()
    if not user:
        flash('User not found')
        return redirect(url_for('auth.index'))

    quiz = Quiz.query.all()

    scores = Score.query.filter_by(user_id=user_id).all()
    max_score=max(score.percentage_score for score in scores)
    min_score=min(score.percentage_score for score in scores)

    scores_list = [score.percentage_score for score in scores]
    quiz_list = [score.quiz.name for score in scores]
    
    return render_template('user/user_summary.html', user=user, quiz=quiz, user_id=user_id, max_score=max_score,
                           min_score=min_score, scores_list=scores_list,quiz_list=quiz_list)