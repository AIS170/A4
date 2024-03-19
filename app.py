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

#db_uri = environ.get('DATABASE_URL')
#if db_uri:
    #app.config['SQLALCHEMY_DATABASE_URI'] = db_uri.replace('postgres://', 'postgresql://', 1)
#else:
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #print("WARNING: 'DATABASE_URL' environment variable is not set. Using SQLite database.")

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
