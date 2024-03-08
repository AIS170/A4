from flask import Flask, render_template
from src.auth import authenticateUser 
from src.user import user_details

app = Flask(__name__)  

@app.route('/')
def home():
    return render_template('index.html')  

app.register_blueprint(authenticateUser, url_prefix='/auth/')

app.register_blueprint(user_details, url_prefix='/user/')

if __name__ == '__main__':  # Correct equality check for the special variable
    app.run(debug=False)
