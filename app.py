from flask import Flask, render_template
from src.auth import authenticateUser

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/a4/')
def index():
    return render_template('index.html')

app.register_blueprint(authenticateUser)

if __name__ == '__main__':
    app.run(debug=True)