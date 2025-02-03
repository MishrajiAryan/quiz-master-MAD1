from flask import Flask, render_template, request, redirect, url_for, flash, session
from app import app
from models import db, User, Subject, Chapter, Quiz, Question, Score, Admin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv
from functools import wraps

# Decorator
def auth_req(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'email' in session:
            return f(*args,**kwargs)
        else:
            flash('Please login to continue')
            return redirect(url_for('login'))
    return inner

def admin_req(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'email' not in session:
            flash('Please login to continue')
            return redirect(url_for('login'))
            
        user=User.query.filter_by(email=session['email']).first()
        if user in session:
            flash('Access Denied')
            return redirect(url_for('index'))
        
        admin = Admin.query.filter_by(email=session['email']).first()
        if not admin:
            flash('Access Denied')
            return redirect(url_for('index'))
        
        return f(*args,**kwargs)
    return inner
        
# the decorator @app.route is directing towards root dir '/'
@app.route('/')
@auth_req
def index():
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        return render_template('admin.html')

    else:
        user=User.query.filter_by(email=session['email']).first()
        return render_template('index.html', user=user)

@app.route('/login')
def login():
    return render_template('login.html')

# login post method
@app.route('/login', methods={'POST'})
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('Please fill all the fields')
        return redirect(url_for('login'))

    # admin login
    admin = Admin.query.filter_by(email=email).first()
    if admin:
        if not check_password_hash(admin.password, password):
            flash('Incorrect Password')
            return redirect(url_for('login'))
        session['email'] = admin.email
        flash('Logged in as Admin')
        return redirect(url_for('index'))

    # user login
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Email does not exist')
        return redirect(url_for('login'))

    if not check_password_hash(user.password, password):
        flash('Incorrect Password')
        return redirect(url_for('login'))

    session['email'] = user.email
    flash('Login Successful')
    return redirect(url_for('index'))

@app.route('/register')
def register():
    return render_template('register.html')

# register post method
@app.route('/register', methods={'POST'})
def register_post():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    name = request.form.get('name')
    qualification = request.form.get('qualification')
    dob = request.form.get('dob')

    if email.lower() == os.getenv('ADMIN_EMAIL'):
        flash('Admin registration is not allowed!')
        return redirect(url_for('register'))
    else:
        if not email or not password or not confirm_password or not name or not qualification or not dob:
            flash('Please fill all the fields')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        # to check for unique prospect
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists')
            return redirect(url_for('register'))

        dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
        password_hash = generate_password_hash(password)
        new_user = User(email=email, password=password_hash,
                        name=name, qualification=qualification, dob=dob_date)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

@app.route('/profile')
@auth_req
def profile():
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        return render_template('profile.html')
    else:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('profile.html', user=user)
    
@app.route('/profile', methods={'POST'})
@auth_req
def profile_post():
    password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_new_password = request.form.get('confirm_new_password')
    new_name = request.form.get('new_name')
    new_qualification = request.form.get('new_qualification')
    new_dob = request.form.get('new_dob')

    if not password:
        flash('Please fill current password before changing anything')
        return redirect(url_for('profile'))
    
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        if not check_password_hash(admin.password, password):
            flash('Incorrect Password')
            return redirect(url_for('profile'))
        
        if new_password:
            if new_password == confirm_new_password:
                new_password_hash = generate_password_hash(new_password)
                admin.password = new_password_hash
            else:
                flash('New Password does not match Confirm Password')
                return redirect(url_for('profile'))
    else:
        user=User.query.filter_by(email=session['email']).first()
        if not check_password_hash(user.password, password):
            flash('Incorrect Password')
            return redirect(url_for('profile'))
        
        if new_password:
            if new_password == confirm_new_password:
                new_password_hash = generate_password_hash(new_password)
                user.password = new_password_hash
            else:
                flash('New Password does not match Confirm Password')
                return redirect(url_for('profile'))
    
        if new_name:
            user.name = new_name
            
        if new_qualification and new_qualification != "Choose...":
            user.qualification = new_qualification
            
        if new_dob:
            new_dob_date = datetime.strptime(new_dob, "%Y-%m-%d").date()
            user.dob = new_dob_date

    db.session.commit()
    flash('Profile Updated successfully')
    return redirect(url_for('profile'))
 
@app.route('/logout')
@auth_req
def logout():
    session.pop('email')
    return redirect(url_for('login'))


'''Below are the pages of Admin'''

@app.route('/admin')
@admin_req
def admin():
    return render_template('admin.html')

@app.route('/subject/add')
@admin_req
def add_subject():
    return 'sub adder'

@app.route('/subject/<int:id>')
@admin_req
def view_subject(id):
    return "view"

@app.route('/subject/<int:id>/delete')
@admin_req
def delete_subject(id):
    return "delete"