from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from src.auth import authenticateUser 
from src.user import user_details
from src.mailbox import mailbox
from src.clear import clear

import sys


app = Flask(__name__)  

@app.route('/')
def home():
    return render_template('index.html')  

app.register_blueprint(authenticateUser, url_prefix='/auth/')

app.register_blueprint(user_details, url_prefix='/user/')

app.register_blueprint(mailbox, url_prefix='/mailbox/')

if __name__ == '__main__':  
    app.run(debug=True)
