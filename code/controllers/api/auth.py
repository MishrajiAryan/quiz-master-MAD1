from flask import render_template, request, redirect, url_for, flash, session, Blueprint, jsonify 
from models import db, User,Admin
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime
import os
from controllers.auth.user_auth import auth_req

auth_bp = Blueprint('auth', __name__)

# the decorator @app.route is directing towards root dir '/'
# Index Page or HomePage
@auth_bp.route('/')
@auth_req
def index():
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        return redirect(url_for('admin.admin'))

    else:
        return redirect(url_for('user.user'))


# Login Page
@auth_bp.route('/login')
def login():
    if 'email' in session:
        admin = Admin.query.filter_by(email=session['email']).first()
        if admin:
            flash('Already logged in as Admin - Logout first to login into another account')
            return redirect(url_for('admin.admin'))
        
        user = User.query.filter_by(email=session['email']).first()
        if user:
            flash('Already logged in - Logout first to login into another account')
            return redirect(url_for('user.user'))
    
    return render_template('auth/login.html')

# login post method
@auth_bp.route('/login', methods={'POST'})
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('Please fill all the fields')
        return redirect(url_for('auth.login'))

    # admin login
    admin = Admin.query.filter_by(email=email).first()
    if admin:
        if not check_password_hash(admin.password, password):
            flash('Incorrect Password')
            return redirect(url_for('auth.login'))
        session['email'] = admin.email
        flash('Log in as Admin successful')
        return redirect(url_for('auth.index'))

    # user login
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Email does not exist')
        return redirect(url_for('auth.login'))

    if not check_password_hash(user.password, password):
        flash('Incorrect Password')
        return redirect(url_for('auth.login'))
    
    is_active= user.is_active

    if is_active == False:
        flash('User access revoked by Admin. Please contact us for further actions')
        return redirect(url_for('auth.login'))


    session['email'] = user.email
    flash('Login Successful')
    return redirect(url_for('auth.index'))

# Register Page
@auth_bp.route('/register')
def register():
    if 'email' in session:
        admin = Admin.query.filter_by(email=session['email']).first()
        if admin:
            flash('Already logged in as Admin - Logout first to login into another account')
            return redirect(url_for('admin.admin'))
        
        user = User.query.filter_by(email=session['email']).first()
        if user:
            flash('Already logged in - Logout first to login into another account')
            return redirect(url_for('user.user'))
        
    return render_template('auth/register.html')

# register post method
@auth_bp.route('/register', methods={'POST'})
def register_post():
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    name = request.form.get('name')
    qualification = request.form.get('qualification')
    dob = request.form.get('dob')

    if email.lower() == os.getenv('ADMIN_EMAIL'):
        flash('Admin registration is not allowed!')
        return redirect(url_for('auth.register'))
    else:
        if not email or not password or not confirm_password or not name or not qualification or not dob or not phone_number:
            flash('Please fill all the fields')
            return redirect(url_for('auth.register'))
    
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('auth.register'))

        # to check for unique prospect
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists')
            return redirect(url_for('auth.register'))
        
        existing_phone = User.query.filter_by(phone_number=phone_number).first()
        if existing_phone:
            flash('Phone number already exists')
            return redirect(url_for('auth.register'))

        dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
        password_hash = generate_password_hash(password)
        new_user = User(email=email, password=password_hash,
                        name=name, qualification=qualification, dob=dob_date, phone_number=phone_number)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration Successful')
        flash('Login to continue')
        return redirect(url_for('auth.login'))

# User/Admin profile page
@auth_bp.route('/profile')
@auth_req
def profile():
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        return render_template('base/profile.html',admin=admin)
    else:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('base/profile.html', user=user)

# User/Admin profile page post method
@auth_bp.route('/profile', methods={'POST'})
@auth_req
def profile_post():
    password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_new_password = request.form.get('confirm_new_password')
    new_phone_number = request.form.get('new_phone_number')
    new_name = request.form.get('new_name')
    new_dob = request.form.get('new_dob')
    new_qualification = request.form.get('new_qualification')

    if not password:
        flash('Please fill current password before changing anything')
        return redirect(url_for('auth.profile'))
    
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin:
        if not check_password_hash(admin.password, password):
            flash('Incorrect Current Password')
            return redirect(url_for('auth.profile'))
        
        if new_password:
            if new_password == confirm_new_password:
                new_password_hash = generate_password_hash(new_password)
                admin.password = new_password_hash
            else:
                flash('New Password does not match Confirm Password')
                return redirect(url_for('auth.profile'))
    else:
        user=User.query.filter_by(email=session['email']).first()
        if not check_password_hash(user.password, password):
            flash('Incorrect Password')
            return redirect(url_for('auth.profile'))
        
        if new_password:
            if new_password == confirm_new_password:
                new_password_hash = generate_password_hash(new_password)
                user.password = new_password_hash
            else:
                flash('New Password does not match Confirm Password')
                return redirect(url_for('auth.profile'))
    
        if new_name:
            user.name = new_name
            
        if new_phone_number:
            existing_phone = User.query.filter_by(phone_number=new_phone_number).first()
            if existing_phone:
                flash('Phone number already exists')
                return redirect(url_for('auth.profile'))
            
            user.phone_number = new_phone_number
            
        if new_dob:
            new_dob_date = datetime.strptime(new_dob, "%Y-%m-%d").date()
            user.dob = new_dob_date

        if new_qualification != "Choose...":
            user.qualification = new_qualification

    db.session.commit()
    flash('Profile Updated successfully')
    return redirect(url_for('auth.profile'))

# Logout 
@auth_bp.route('/logout')
@auth_req
def logout():
    session.pop('email')
    flash('Log Out Successful')
    return redirect(url_for('auth.login'))

