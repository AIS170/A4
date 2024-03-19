from .database import db
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from .models import User, Token
import uuid
import re
import os


authenticateUser = Blueprint('authenticate_user', __name__)

@authenticateUser.route('/signup/', methods=['GET', 'POST'])
# Registers a new user and redirects them to their mailbox
def signup():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400
        elif len(first_name) > 15:
            return jsonify({'error': 'First name cannot exceed 15 characters'}), 400
        elif len(first_name) == 0:
            return jsonify({'error': 'First name cannot be empty'}), 400
        elif len(last_name) > 15:
            return jsonify({'error': 'Last name cannot exceed 15 characters'}), 400
        elif len(last_name) == 0:
            return jsonify({'error': 'Last name cannot be empty'}), 400
        elif not validEmail(email):
            return jsonify({'error': 'Email must be of a valid format'}), 400
        elif len(password) < 8:
            return jsonify({'error': 'Password should be atleast 8 characters'}), 400
        elif len(password) > 15:
            return jsonify({'error': 'Password shouldn\'t exceed 15 characters'}), 400
        elif not (any(char.isalpha() for char in password) and any(char.isdigit() for char in password)):
            return jsonify({'error': 'Password should contain atleast one letter and one number'}), 400
        else:
            user_id = str(uuid.uuid4())
            new_user = User(id=user_id, first_name=first_name, last_name=last_name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for('authenticate_user.login'))
    return render_template('register.html')

# Helper function to check if an email is of valid format
def validEmail(email: str) -> bool:
    regexPattern = r'^[a-zA-Z0-9._]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$'
    if re.match(regexPattern, email):
        return True
    else:
        return False


# Login page for registered users. Redirects the user to their mailbox
@authenticateUser.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        input_password = request.form.get('password')

        if user and user.password == input_password:
            session_token = os.urandom(24).hex()
            session['user_id'] = user.id
            session['session_token'] = session_token
        
            token_entry = Token.query.filter_by(user_id=user.id).first()
            if token_entry:
                token_entry.id = session_token
            else:
                token_entry = Token(id=session_token, user_id=user.id)
                db.session.add(token_entry)
            
            db.session.commit()

            return redirect(url_for('mailbox_route.mailBox'))
        else:
            return jsonify({'error': 'Invalid email and/or password'}), 400
    else:
        return render_template('login.html')
    
@authenticateUser.route('/logout')
# Ends the current users session and redirects them to the login page
def userLogout():
    user_id = session.get('user_id')
    if user_id:
        token_entry = Token.query.filter_by(user_id=user_id).first()
        
        if token_entry:
            db.session.delete(token_entry)
            db.session.commit()
    session.clear()
    return redirect(url_for('authenticate_user.login'))