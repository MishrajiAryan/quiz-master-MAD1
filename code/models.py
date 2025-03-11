from app import app
from flask_sqlalchemy import SQLAlchemy # type: ignore
from datetime import datetime
import os
from werkzeug.security import generate_password_hash # type: ignore
from dotenv import load_dotenv # type: ignore

db = SQLAlchemy(app)
load_dotenv()


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    # Store hashed passwords
    password = db.Column(db.String(256), nullable=False)


def create_admin():
    with app.app_context():
        admin_email = os.getenv('ADMIN_EMAIL')
        admin_password = os.getenv('ADMIN_PASSWORD')

        if not Admin.query.filter_by(email=admin_email).first():
            admin_user = Admin(email=admin_email,password=generate_password_hash(admin_password))
            db.session.add(admin_user)
            db.session.commit()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True)
    # Store hashed passwords
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100))
    dob = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.today(), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)



class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.today())

    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade="all, delete")


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.today())

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id', ondelete="CASCADE"), nullable=False)  # Add CASCADE
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration = db.Column(db.String(10))  # HH:MM format
    remarks = db.Column(db.Text)

    chapter = db.relationship('Chapter', backref=db.backref('quizzes', lazy=True, cascade="all, delete"))
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete")



class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(200), nullable=False)
    option2 = db.Column(db.String(200), nullable=False)
    option3 = db.Column(db.String(200))
    option4 = db.Column(db.String(200))
    correct_option = db.Column(db.Integer, nullable=False)  # 1,2,3,4


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.today())
    total_score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage_score = db.Column(db.Float, nullable=False)

    quiz = db.relationship('Quiz', backref=db.backref('scores', lazy=True))
    user = db.relationship('User', backref=db.backref('scores', lazy=True))


with app.app_context():
    db.create_all()
    create_admin()
