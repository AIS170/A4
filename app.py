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


EXTERNAL_API_URL = "https://ubl-invoice-generator.vercel.app"

@app.route('/external_api')
def external_api_page():
    return render_template('external_api.html')

@app.route('/external_api/text_file', methods=['POST'])
def create_invoice_text_file():
    try:
        # Extract file from the request
        file = request.files['file']
        
        # Pass file to external API
        response = requests.post(EXTERNAL_API_URL + "/invoices/create/user/textFile", files={'file': file})
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Assuming the API returns JSON data, you can extract it like this
        data = response.json()

        return render_template('create_invoice_text.html', data=data)
    except Exception:
        return jsonify({'error': 'Failed to get textFile link for invoice creation'}, 500)

@app.route('/external_api/gui', methods=['GET'])
def get_invoice_creation_gui_link():
    try:
        # Make request to external API
        response = requests.get(EXTERNAL_API_URL + "/invoices/create/user/gui")
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Assuming the API returns JSON data, you can extract it like this
        data = response.json()

        return render_template('guest_gui.html', data=data), 200
    except Exception:
        return jsonify({'error': 'Failed to get textFile link for invoice creation'}, 500)

@app.route('/external_api/database', methods=['POST'])
def create_invoice_from_database():
    try:
        # Extract parameters from the request
        search_string = request.args.get('searchString')
        skip = request.args.get('skip', default=0, type=int)
        limit = request.args.get('limit', default=50, type=int)

        # Pass parameters to external API
        response = requests.post(EXTERNAL_API_URL + "/invoices/create/user/dataBase",
                                 params={'searchString': search_string, 'skip': skip, 'limit': limit})
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Assuming the API returns JSON data, you can extract it like this
        data = response.json()

        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        app.logger.error('Failed to create invoice from database: %s', e)
        return jsonify({'error': 'Failed to create invoice from database'}), 500

@app.route('/external_api/guest_image', methods=['POST'])
def create_invoice_from_image():
    try:
        # Extract file from the request
        pdf_file = request.files['pdf']

        # Pass file to external API
        response = requests.post(EXTERNAL_API_URL + "/invoices/create/guest/image", files={'pdf': pdf_file})
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Assuming the API returns JSON data, you can extract it like this
        data = response.json()

        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        app.logger.error('Failed to create invoice from image: %s', e)
        return jsonify({'error': 'Failed to create invoice from image'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=environ.get('PORT', 5050))

