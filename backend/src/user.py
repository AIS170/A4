from .database import db
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from .models import User

user_route = Blueprint('user_route', __name__)

@user_route.route('/details', methods=['GET'])
def details():
    user_id_a = session.get('user_id')
    #error check needed
    user = User.query.get(user_id_a)

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
    user = User.query.get(user_id_a)
    new_email = request.form.get('new_email')
    user.email = new_email
    db.session.commit()
    return redirect(url_for('user_route.details'))

@user_route.route('/password', methods=['PUT'])
def password():
    user_id_a = session.get('user_id')
    user = User.query.get(user_id_a)
    new_password = request.form.get('new_password')
    user.password = new_password
    db.session.commit()
    return redirect(url_for('user_route.details'))
