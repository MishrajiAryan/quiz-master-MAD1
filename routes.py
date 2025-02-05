from re import sub
from unicodedata import category
from unittest import removeResult
from flask import Flask, render_template, request, redirect, url_for, flash, session
from app import app
from models import db, User, Subject, Chapter, Quiz, Question, Score, Admin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv
from functools import wraps

# Decorator for Authentication
def auth_req(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'email' in session:
            return f(*args,**kwargs)
        else:
            flash('Please login to continue')
            return redirect(url_for('login'))
    return inner

# Decorator for Admin Authentication
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
# Index Page or HomePage
@app.route('/')
@auth_req
def index():
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        return redirect(url_for('admin'))

    else:
        user=User.query.filter_by(email=session['email']).first()
        return render_template('index.html', user=user)

# Login Page
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

# Register Page
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

# User/Admin profile page
@app.route('/profile')
@auth_req
def profile():
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        return render_template('profile.html')
    else:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('profile.html', user=user)

# User/Admin profile page post method
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

# Logout 
@app.route('/logout')
@auth_req
def logout():
    session.pop('email')
    return redirect(url_for('login'))


'''Below are the pages of Admin'''

@app.route('/admin')
@admin_req
def admin():
    subjects = Subject.query.all()
    return render_template('admin.html', subjects=subjects)

'''Subject Related Pages'''

@app.route('/subject/add')
@admin_req
def add_subject():
    return render_template('/subject/add_subject.html')

@app.route('/subject/add', methods=['POST'])
@admin_req
def add_subject_post():
    name = request.form.get('subject_name')
    description = request.form.get('subject_description')

    if not description or not name:
        flash('Please fill all the fields')
        return redirect(url_for('add_subject'))
    
    existing_subject = Subject.query.filter(Subject.name == name).first()

    if existing_subject:
        flash('Subject name already exists, choose another')
        return redirect(url_for('add_subject'))

    
    subject = Subject(name=name, description=description)
    db.session.add(subject)
    db.session.commit()
    flash("Subject Added Successfully")

    return redirect(url_for('admin'))

@app.route('/subject/<int:subject_id>')
@admin_req
def view_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin'))
    return render_template('/subject/view_subject.html',subject=subject)

@app.route('/subject/<int:subject_id>/edit')
@admin_req
def edit_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin'))
    return render_template('/subject/edit_subject.html', subject=subject)

@app.route('/subject/<int:subject_id>/edit', methods=['POST'])
@admin_req
def edit_subject_post(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin'))
    
    name = request.form.get('subject_name')
    description = request.form.get('subject_description')

    if not description or not name:
        flash('Please fill all the fields')
        return redirect(url_for('edit_subject', subject_id=subject_id))
    
    subject.name = name
    subject.description = description

    db.session.commit()

    flash("Subject Updated Successfully")
    return redirect(url_for('admin'))

@app.route('/subject/<int:subject_id>/delete')
@admin_req
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin'))
    return render_template('/subject/delete_subject.html',subject=subject)

@app.route('/subject/<int:subject_id>/delete', methods=['POST'])
@admin_req
def delete_subject_post(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin'))
    db.session.delete(subject)
    db.session.commit()

    flash('Subject Deleted Successfully')
    return redirect(url_for('admin'))

'''Chapters Related Pages'''

@app.route('/subject/<int:subject_id>/chapter/add')
@admin_req
def add_chapter(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject does not exist')
        return redirect(url_for('admin'))
    return render_template('/chapter/add_chapter.html', subject=subject)


@app.route('/subject/<int:subject_id>/chapter/add', methods=['POST'])
@admin_req
def add_chapter_post(subject_id):
    subject = Subject.query.get(subject_id)
    name = request.form.get('chapter_name')
    description = request.form.get('chapter_description')

    if not description or not name:
        flash('Please fill all the fields')
        return redirect(url_for('add_chapter', subject_id=subject.id))
    
    chapter = Chapter(name=name, description=description, subject_id=subject.id)
    db.session.add(chapter)
    db.session.commit()
    flash("Chapter Added Successfully")

    return redirect(url_for('view_subject', subject_id=subject.id))


@app.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/delete')
@admin_req
def delete_chapter(subject_id, chapter_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject does not exist')
        return redirect(url_for('admin'))
    
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('view_subject', subject_id=subject_id))
    
    return render_template('/chapter/delete_chapter.html',subject=subject, chapter=chapter)


@app.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/delete', methods=['POST'])
@admin_req
def delete_chapter_post(subject_id,chapter_id):
    subject = Subject.query.get(subject_id)
    
    if not subject:
        flash('Subject does not exist')
        return redirect(url_for('admin'))
    
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('view_subject', subject_id=subject_id))
    
    db.session.delete(chapter)
    db.session.commit()

    flash('Chapter Deleted Successfully')
    return redirect(url_for('view_subject', subject_id=subject_id))


@app.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/edit')
@admin_req
def edit_chapter(subject_id,chapter_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin'))

    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('view_subject', subject_id=subject_id))
    
    return render_template('/chapter/edit_chapter.html', subject=subject, chapter=chapter)

@app.route('/subject/<int:subject_id>/chapter/<int:chapter_id>/edit', methods=['POST'])
@admin_req
def edit_chapter_post(subject_id,chapter_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found')
        return redirect(url_for('admin'))
    
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash('Chapter does not exist')
        return redirect(url_for('view_subject', subject_id=subject_id))
    
    name = request.form.get('chapter_name')
    description = request.form.get('chapter_description')

    if not description or not name:
        flash('Please fill all the fields')
        return redirect(url_for('edit_chapter',subject_id=subject_id, chapter_id=chapter_id))
    
    chapter.name = name
    chapter.description = description

    db.session.commit()

    flash("Chapter Updated Successfully")
    return redirect(url_for('view_subject', subject_id=subject_id))



'''Quiz Related Pages'''