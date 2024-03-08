from flask import Flask, render_template
from importlib_resources import path
from src.auth import authenticateUser 
from src.user import user_details
from flask_sqlalchemy import SQLAlchemy
from src.models import User

db = SQLAlchemy()
DB_NAME = "database_db"
app = Flask(__name__)  
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

@app.route('/')
def home():
    return render_template('index.html')  

app.register_blueprint(authenticateUser, url_prefix='/auth/')

app.register_blueprint(user_details, url_prefix='/user/')

if not path.exists('src/' + DB_NAME):
    db.create_all(app)
    print('Created database')
    

if __name__ == '__main__':  # Correct equality check for the special variable
    app.run(debug=False)
