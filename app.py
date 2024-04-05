from flask import Flask, jsonify, render_template, request
import requests
from backend.src.auth import authenticateUser 
from backend.src.database import db
from backend.src.mailbox import mailbox
from backend.src.clear import clear_
from backend.src.reports import reports
from backend.src.user import user_route
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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/tracking')
def track():
    return render_template('track.html')

app.register_blueprint(authenticateUser, url_prefix='/auth/')
     
app.register_blueprint(mailbox, url_prefix='/mailbox/')  

app.register_blueprint(clear_, url_prefix='/clear')

app.register_blueprint(reports, url_prefix='/reports/')

app.register_blueprint(user_route, url_prefix='/user/')


EXTERNAL_API_URL = "http://3.27.23.157"

@app.route('/external_api')
def external_api_page():
    deployment_link = EXTERNAL_API_URL  # Your deployment link
    return render_template('external_api.html', deployment_link=deployment_link)

@app.route('/external_api/CSV', methods=['GET','POST'])
def create_invoice_text_file():
    try:
        # Forward the request to the external API yo
        response = requests.post("http://3.27.23.157/invoice/CSV/", data=request.form)

        # Assuming the API returns JSON data, you can extract it like this
        data = response.json()

        return render_template('create_invoice_text.html', data=data)
    except Exception:
        return jsonify({'error': 'Failed to get textFile link for invoice creation'}, 500)

 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=environ.get('PORT', 5000))

