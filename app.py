from flask import Flask, render_template
from src.auth import authenticateUser  # This should define a Blueprint named, for example, `auth_blueprint`

app = Flask(__name__)  # Correct initialization with double underscores

@app.route('/')
def home():
    return render_template('index.html')  # Correct function name

app.register_blueprint(authenticateUser, url_prefix='/auth/')  # Assume 'authenticateUser' is a Blueprint object

if __name__ == '__main__':  # Correct equality check for the special variable
    app.run(debug=False)
