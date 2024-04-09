
from flask import Flask, jsonify, render_template, request
import requests # type: ignore

from backend.src.auth import authenticateUser 
from backend.src.database import db
from backend.src.mailbox import mailbox
from backend.src.clear import clear_
from backend.src.reports import reports
from backend.src.user import user_route
from backend.src.create_invoice import create_invoice
from os import environ
from flask_cors import CORS # type: ignore
from os import path
import os


DB_NAME = 'database.sqlite3'

app = Flask(__name__)

app.config['SECRET_KEY'] = 'zasdxfcgvhbjnknhbgvfcdretfygh'

#db_uri = environ.get('DATABASE_URL')  yo
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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

app.register_blueprint(authenticateUser, url_prefix='/auth/')
     
app.register_blueprint(mailbox, url_prefix='/mailbox/')  

app.register_blueprint(clear_, url_prefix='/clear')

app.register_blueprint(reports, url_prefix='/reports/')

app.register_blueprint(user_route, url_prefix='/user/')

app.register_blueprint(create_invoice, url_prefix='/invoice/')
 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=environ.get('PORT', 5000))

