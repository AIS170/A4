from .database import db
from flask import Blueprint, render_template, request, redirect, \
                  url_for, jsonify, session, current_app
from .models import User
from werkzeug.utils import secure_filename
import re
import os


user_route = Blueprint('user_route', __name__)


# Retrieves the user's registration details
@user_route.route('/details', methods=['GET'])
def details():
    user_id_a = session.get('user_id')
    if user_id_a is None:
        return jsonify({'error': 'Invalid userId'}), 400
    user = User.query.filter_by(id=user_id_a).first()

    user_details = {
        'image_file': user.image_file,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'password': user.password,
    }
    return render_template('user.html', user=user_details), 200


# Allows the user to change their email
@user_route.route('/email', methods=['PUT'])
def email():
    user_id_a = session.get('user_id')
    if user_id_a is None:
        return jsonify({'error': 'Invalid userId'}), 400
    user = User.query.filter_by(id=user_id_a).first()
    new_email = request.form.get('new_email')
    if not validEmail(new_email):
        return jsonify({'error': 'Email must be of a valid format'}), 400
    elif user.email == new_email:
        return jsonify(
            {'error': 'New email is the same as current email'}
        ), 400
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


# Allows the user to change their password
@user_route.route('/password', methods=['PUT'])
def password():
    user_id_a = session.get('user_id')
    if user_id_a is None:
        return jsonify({'error': 'Invalid userId'}), 400
    user = User.query.filter_by(id=user_id_a).first()
    new_password = request.form.get('new_password')
    if len(new_password) < 8:
        return jsonify(
            {'error': 'Password should be atleast 8 characters'}
        ), 400
    elif len(new_password) > 15:
        return jsonify(
            {'error': 'Password shouldn\'t exceed 15 characters'}
        ), 400
    elif not (any(char.isalpha() for char in new_password) and
              any(char.isdigit() for char in new_password)):
        return jsonify(
            {'error': 'Password should contain atleast one letter and one '
             'number'}), 400
    user.password = new_password
    db.session.commit()
    return redirect(url_for('user_route.details'))


# Allows the user to change their profile picture
@user_route.route('/update-profile-picture', methods=['POST'])
def update_profile_picture():
    user_id_a = session.get('user_id')
    if user_id_a is None:
        return jsonify({'error': 'Invalid userId'}), 400

    user = User.query.filter_by(id=user_id_a).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if ('.' not in file.filename or
       file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions):
        return jsonify({'error': 'Invalid file extension'}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    user.image_file = filename
    db.session.commit()

    return redirect(url_for('user_route.details'))
