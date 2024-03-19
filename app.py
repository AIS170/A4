from flask import Flask, render_template
from src.auth import authenticateUser 
# from src.user import user_details
from src.database import db
from src.mailbox import mailbox
from src.clear import clear_
# from .models import User
from os import environ
from flask_cors import CORS



from os import path

DB_NAME = 'database.sqlite3'

app = Flask(__name__)  

app.config['SECRET_KEY'] = 'zasdxfcgvhbjnknhbgvfcdretfygh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://u1c1i80rmavav3:p4bc646acbe4e80e77c0d7bbde28a39c06ecb5ac70145f6d5c46dc0348ae2adaf@ceu9lmqblp8t3q.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dabgngmnllkkfv' or f'sqlite:///{DB_NAME}'

db.init_app(app)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')  

app.register_blueprint(authenticateUser, url_prefix='/auth/')
     
app.register_blueprint(mailbox, url_prefix='/mailbox/')  

app.register_blueprint(clear_, url_prefix='/clear')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=environ.get('PORT', 5000))
