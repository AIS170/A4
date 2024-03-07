# Stub code for authorisation functions
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import uuid
import re

authenticateUser = Blueprint('authenticate_user', __name__)

@authenticateUser.route('/signup/', methods=['GET', 'POST'])
# Registers a new user and redirects them to their mailbox
def signup():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
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
            user_id = uuid.uuid4()
            return jsonify({'userId': user_id}), 200
    return render_template('register.html')

def validEmail(email: str) -> bool:
    regexPattern = r'^[a-zA-Z0-9._]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$'
    if re.match(regexPattern, email):
        return True
    else:
        return False


# Login page for registered users. Redirects the user to their mailbox
# @authenticateUser.route('/login/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # email, password
#         return 'u1'
#     return render_template('login.html')
