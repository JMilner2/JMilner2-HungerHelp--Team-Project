"""
Author: Shaikha + Vilius
Description: This module defines Flask routes for user registration, login, logout, profile, and settings.
 It also includes form validation, user authentication, and logging events.
"""
import bcrypt
from flask import Blueprint, render_template, redirect, url_for, flash, session, Markup, request
from app import db, requires_roles
from models import User
from users.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
import logging


users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash('Email address already exists')
            return render_template('users/register.html', form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        phone=form.phone.data,
                        password=form.password.data,
                        notifications=form.notifications.data,
                        role='user')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Logging an event for user registration
        logging.warning('SECURITY - User registration [%s, %s]',
                        form.email.data, request.remote_addr)

        return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # checking if the key-value pair is in the session, and adding it if not
    if not session.get('attempts'):
        # counting authentication attempts
        session['attempts'] = 0

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # check if user exists, password is correct and one-time password is correct
        if not user or not bcrypt.checkpw(form.password.data.encode('utf-8'), user.password):
            session['attempts'] += 1

            # Logging an event for user invalid login
            logging.warning('SECURITY - Invalid log in [%s, %s]',
                            form.email.data, request.remote_addr)

            # limiting login attempts to only 4 attempts
            if session.get('attempts') >= 4:
                flash(Markup('Number of incorrect login attempts exceeded. '
                             'please click <a href="/reset">here</a> to reset.'))
                return render_template('users/login.html')
            flash('please check your details,{} login attempts remaining'
                  .format(4 - session.get('attempts')))
            return render_template('users/login.html', form=form)

        # if user exists and passwords are correct, logs in user
        login_user(user)

        # Logging an event for user login
        logging.warning('SECURITY - Log in [%s, %s, %s]',
                        current_user.id, current_user.email,
                        request.remote_addr)

        # # update last login and current login time
        user.last_login = user.current_login
        user.current_login = datetime.now()
        db.session.add(user)
        db.session.commit()

        # if statement to redirect user to correct page based on their role
        if current_user.role == 'user':
            return redirect(url_for('blog.blog_home'))
        else:
            return redirect(url_for('admin.admin'))
    return render_template('users/login.html', form=form)


@users_blueprint.route('/reset')
def reset():
    session['attempts'] = 0
    return redirect(url_for('users.login'))


# view user logout
@users_blueprint.route('/logout')
@login_required
@requires_roles('user', 'admin')
def logout():
    # Logging an event for user logout
    logging.warning('SECURITY - Log out [%s, %s, %s]',
                    current_user.id, current_user.email, request.remote_addr)
    logout_user()
    return redirect(url_for('main.index'))


# view user account
@users_blueprint.route('/profile')
@login_required
@requires_roles('user', 'admin')
def profile():
    return render_template('users/profile.html',
                           acc_no=current_user.id,
                           email=current_user.email,
                           firstname=current_user.firstname,
                           lastname=current_user.lastname,
                           phone=current_user.phone)

@users_blueprint.route('/settings')
def settings():
    return render_template('users/settings.html')



