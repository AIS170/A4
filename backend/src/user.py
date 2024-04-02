from .database import db
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from .models import User
import re

user_route = Blueprint('user_route', __name__)

@user_route.route('/details', methods=['GET'])
def details():
    user_id_a = session.get('user_id')
    if user_id_a == None:
        return jsonify({'error': 'Invalid userId'}), 400
    user = User.query.filter_by(id=user_id_a).first()

    user_details = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'password': user.password
    }
    return render_template('user.html', user = user_details), 200

@user_route.route('/email', methods=['PUT'])
def email():
    user_id_a = session.get('user_id')
    if user_id_a == None:
        return jsonify({'error': 'Invalid userId'}), 400
    user = User.query.filter_by(id=user_id_a).first()
    new_email = request.form.get('new_email')
    if not validEmail(new_email):
        return jsonify({'error': 'Email must be of a valid format'}), 400
    elif user.email == new_email:
        return jsonify({'error': 'New email is the same as current email'}), 400
    elif User.query.filter_by(email=new_email).first():
        return jsonify({'error': 'Email is already in use'}), 400
    user.email = new_email
    db.session.commit()
    return redirect(url_for('user_route.details'))

# Helper function to check if an email is of valid format
def validEmail(email):
    regexPattern = r'^[a-zA-Z0-9._]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$'
    if re.match(regexPattern, email):
        return True
    else:
        return False

@user_route.route('/password', methods=['PUT'])
def password():
    user_id_a = session.get('user_id')
    if user_id_a == None:
        return jsonify({'error': 'Invalid userId'}), 400
    user = User.query.filter_by(id=user_id_a).first()
    new_password = request.form.get('new_password')
    if len(new_password) < 8:
        return jsonify({'error': 'Password should be atleast 8 characters'}), 400
    elif len(new_password) > 15:
        return jsonify({'error': 'Password shouldn\'t exceed 15 characters'}), 400
    elif not (any(char.isalpha() for char in new_password) and any(char.isdigit() for char in new_password)):
        return jsonify({'error': 'Password should contain atleast one letter and one number'}), 400
    user.password = new_password
    db.session.commit()
    return redirect(url_for('user_route.details'))
