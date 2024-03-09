from flask import Flask, render_template
from src.auth import authenticateUser
from src.mailbox import mbox

app = Flask(__name__, template_folder='template')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/a4/')
def index():
    return render_template('index.html')

app.register_blueprint(authenticateUser)

app.register_blueprint(mbox, url_prefix='/mailbox/')

if __name__ == '__main__':
    app.run(debug=True)