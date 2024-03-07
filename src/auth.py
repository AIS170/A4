# Stub code for authorisation functions
from flask import Blueprint, render_template, request, redirect, url_for

authenticateUser = Blueprint('authenticate_user', __name__)

@authenticateUser.route('/a4/signup/', methods=['GET', 'POST'])
# Registers a new user and redirects them to their mailbox
def signup():
    if request.method == 'POST':
        # firstName, lastName, email, password, confirmPassword
        return 'u1'
    return render_template('register.html')

# Login page for registered users. Redirects the user to their mailbox
@authenticateUser.route('/a4/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # email, password
        return 'u1'
    return render_template('login.html')
