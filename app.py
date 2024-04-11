
import io
from flask import Flask, jsonify, render_template, request
import requests # type: ignore hi

from backend.src.auth import authenticateUser 
from backend.src.database import db
from backend.src.mailbox import mailbox
from backend.src.clear import clear_
from backend.src.models import Invoice
from backend.src.reports import reports
from backend.src.user import user_route
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

 

def register_user_with_service_account():
    url = "http://rendering.ap-southeast-2.elasticbeanstalk.com/user/register"
    payload = {
        "email": "A4Ecommerce@gmail.com",
        "password": "A4Ecommerce17",
        "first_name": "A4EcommerceUser",
        "last_name": "A$ECOMM"
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        # User registration successful
        return True
    else:
        # Handle registration failure
        return False
    
def login_to_external_api():
    url = "http://rendering.ap-southeast-2.elasticbeanstalk.com/user/login"
    payload = {
        "email": "A4Ecommerce@gmail.com",
        "password": "A4Ecommerce17"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return jsonify({'token': data.get('token')}), 200
    else:
        return jsonify({'error': 'Login failed'}), 401
    


def get_invoice_body(invoice_id):
    invoice = Invoice.query.filter_by(id=invoice_id).first()
    if invoice:
        return invoice.body
    else:
        return None

def send_invoice_as_xml(invoice_body, output_type, language, token):
    if invoice_body:
        url = "http://rendering.ap-southeast-2.elasticbeanstalk.com/render"
        payload = {
            "file": invoice_body,
            "outputType": output_type,
            "language": language,
            "token": token
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.text
        else:
            return None
    else:
        return None

@app.route('/render_invoice', methods=['POST'])
def render_invoice_route():
    data = request.json
    invoice_id = data.get('invoice_id')
    output_type = data.get('output_type')
    language = data.get('language')
    token = data.get('token')

    if not all([invoice_id, output_type, language, token]):
        return jsonify({'error': 'Missing parameters'}), 400

    # Retrieve invoice body from the database
    invoice_body = get_invoice_body(invoice_id)

    # Send invoice for rendering
    rendered_invoice = send_invoice_as_xml(invoice_body, output_type, language, token)
    
    if rendered_invoice:
        return rendered_invoice, 200
    else:
        return jsonify({'error': 'Failed to render invoice'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=environ.get('PORT', 5000))

