from flask import Flask, render_template, request, redirect, url_for, flash
from app import app
from models import db, User, Subject, Chapter, Quiz, Question, Score
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

#the decorator @app.route is directing towards root dir '/'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods={'POST'})
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('Please fill all the fields')
        return redirect(url_for('login'))
    
    user=User.query.filter_by(email=email).first()

    if not user:
        flash('User does not exist')
        return redirect(url_for('login'))
    
    if not check_password_hash(user.password, password):
        flash('Incorrect Password')
        return redirect(url_for('login'))
    
    return redirect(url_for('index'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods={'POST'})
def register_post():
    email= request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    name = request.form.get('name')
    qualification = request.form.get('qualification')
    dob = request.form.get('dob')

    if not email or not password or not confirm_password or not name or not qualification or not dob:
        flash('Please fill all the fields')
        return redirect(url_for('register'))
    
    if password != confirm_password:
        flash('Passwords do not match')
        return redirect(url_for('register'))
    
    user = User.query.filter_by(email=email).first() #to check for unique prospect

    if user:
        flash('Email already exists')
        return redirect(url_for('register'))

    dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
    password_hash = generate_password_hash(password)
    new_user = User(email=email, password=password_hash, name=name,qualification=qualification, dob=dob_date)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))