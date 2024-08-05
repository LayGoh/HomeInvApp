# Import necessary modules from Flask and other packages
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import app, db
from flask_login import login_user, logout_user, login_required, current_user
from .decorators import admin_required
from app.models import User
from app.forms import AdminResetPasswordForm, RegistrationForm, LoginForm, ResetPasswordForm, SecurityQuestionForm
from werkzeug.security import generate_password_hash, check_password_hash

# Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form.get('username').lower()
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

# Logout route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('home'))

# Register route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data.lower()
        password = form.password.data
        security_question = form.security_question.data
        security_answer = form.security_answer.data.lower()
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))
        user_count = User.query.count()
        is_admin = (user_count == 0)
        new_user = User(
            username=username,
            password=hashed_password,
            security_question=security_question,
            security_answer=security_answer,
            is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        flash('Registered successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

# Forgot Password route
@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = SecurityQuestionForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user:
            return redirect(url_for('auth.reset_password', user_id=user.id))
        flash('Username not found', 'danger')
    return render_template('forgot_password.html', form=form)

# Reset Password route
@auth_bp.route('/reset_password/<int:user_id>', methods=['GET', 'POST'])
def reset_password(user_id):
    user = User.query.get_or_404(user_id)
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if form.security_answer.data == user.security_answer:
            user.password = generate_password_hash(form.new_password.data, method='pbkdf2:sha256', salt_length=16)
            db.session.commit()
            flash('Password reset successfully!', 'success')
            return redirect(url_for('auth.login'))
        flash('Security answer incorrect', 'danger')
    return render_template('reset_password.html', form=form, user=user)

# Route for Admin to Reset User Password
@app.route('/reset_user_password/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def reset_user_password(user_id):
    form = AdminResetPasswordForm
    user = User.query.get_or_404(user_id)
    new_password = generate_password_hash('Avery', method='pbkdf2:sha256', salt_length=16)
    user.password = new_password
    db.session.commit()
    flash('User password reset to "Avery"', 'success')
    return redirect(url_for('admin'))
