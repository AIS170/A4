from flask import Flask, render_template, redirect, url_for
from backend.src.tracking import tracking
from backend.src.render_invoice import render_invoice
from backend.src.create_invoice import create_invoice
from backend.src.auth import authenticateUser, logout
from backend.src.database import db
from backend.src.mailbox import mailbox
from backend.src.clear import clear_
from backend.src.reports import reports
from backend.src.user import user_route
from flask_cors import CORS
from os import environ
import os

DB_NAME = 'database.sqlite3'

app = Flask(__name__)

app.config['SECRET_KEY'] = 'zasdxfcgvhbjnknhbgvfcdretfygh'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

app.config['UPLOAD_FOLDER'] = 'static/profile_pictures'
UPLOAD_PATH = os.path.join(os.getcwd(), 'static', 'profile_pictures')
if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)

db.init_app(app)
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/pricing')
def price():
    return render_template('price.html')


@app.route('/auth/logout')
def userLogout():
    token = logout()
    if token:
        db.session.delete(token)
        db.session.commit()
    return redirect(url_for('authenticate_user.login'))


@app.route('/download')
def download_invoice():
    return render_template('download.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


app.register_blueprint(authenticateUser, url_prefix='/auth/')

app.register_blueprint(mailbox, url_prefix='/mailbox/')

app.register_blueprint(reports, url_prefix='/reports/')

app.register_blueprint(clear_, url_prefix='/clear')

app.register_blueprint(create_invoice, url_prefix='/invoice/')

app.register_blueprint(user_route, url_prefix='/user/')

app.register_blueprint(render_invoice, url_prefix='/render/')

app.register_blueprint(tracking, url_prefix='/tracking/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=environ.get('PORT', 5000))
