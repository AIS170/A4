
import io
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import requests # type: ignore hi

from backend.src.auth import authenticateUser, register, logout 
from backend.src.database import db
from backend.src.mailbox import mailbox
from backend.src.clear import clear_
from backend.src.models import Invoice, User
from backend.src.reports import getReports
from backend.src.user import user_route
from backend.src.create_invoice import create_invoice
from os import environ
from flask_cors import CORS # type: ignore
from os import path
import os


DB_NAME = 'database.sqlite3'

app = Flask(__name__)

app.config['SECRET_KEY'] = 'zasdxfcgvhbjnknhbgvfcdretfygh'

#db_uri = environ.get('DATABASE_URL')  yo hei
#if db_uri:
    #app.config['SQLALCHEMY_DATABASE_URI'] = db_uri.replace('postgres://', 'postgresql://', 1)
#else:
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #print("WARNING: 'DATABASE_URL' environment variable is not set. Using SQLite database.")

app.config['UPLOAD_FOLDER'] = 'static/profile_pictures'
UPLOAD_PATH = os.path.join(os.getcwd(), 'static', 'profile_pictures')
if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)

db.init_app(app)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')  


@app.route('/auth/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        user_id_a = register()
        new_user = User(id=user_id_a, first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('authenticate_user.login'))
    return render_template('register.html')


@app.route('/auth/logout')
def userLogout():
    token = logout()
    if token:
        db.session.delete(token)
        db.session.commit()
    return redirect(url_for('authenticate_user.login'))

@app.route('/reports', methods=['GET'])
def reportBox():
    formatted_reports = getReports()
    return render_template('report.html', formatted_reports=formatted_reports)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

app.register_blueprint(authenticateUser, url_prefix='/auth/')
     
app.register_blueprint(mailbox, url_prefix='/mailbox/')  

app.register_blueprint(clear_, url_prefix='/clear')



app.register_blueprint(user_route, url_prefix='/user/')


app.register_blueprint(create_invoice, url_prefix='/invoice/')
 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=environ.get('PORT', 5000))

