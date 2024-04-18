import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from backend.src.models import User, Token
import json

BASE_URL = "http://localhost:5000"

# Define valid test data
valid_registration_data1 = {
    "firstName": "First",
    "lastName": "User",
    "email": "user@example.com",
    "password": "val1dPassword",
    "confirmPassword": "val1dPassword"
}

valid_registration_data2 = {
    "firstName": "Second",
    "lastName": "User",
    "email": "user2@example.com",
    "password": "val1dPassword",
    "confirmPassword": "val1dPassword"
}

valid_login_data = {
    "email": "user@example.com",
    "password": "val1dPassword",
}

# ================================================
# ======= Test Cases for the Signup route ========
# ================================================


# Test successful user registration
def test_signup_success():
    client = app.test_client()
    client.delete('/clear')
    response1 = client.post(
        '/auth/signup',
        data=valid_registration_data1,
        follow_redirects=True
    )
    assert response1.status_code == 200

    with app.app_context():
        user = User.query.filter_by(
            email=valid_registration_data1['email']
        ).first()
        assert user is not None


def test_signup_success_two_users():
    client = app.test_client()
    client.delete('/clear')
    response1 = client.post(
        '/auth/signup',
        data=valid_registration_data1,
        follow_redirects=True
    )
    assert response1.status_code == 200
    response2 = client.post(
        '/auth/signup',
        data=valid_registration_data2,
        follow_redirects=True
    )
    assert response2.status_code == 200

    with app.app_context():
        user1 = User.query.filter_by(
            email=valid_registration_data1['email']
        ).first()
        user2 = User.query.filter_by(
            email=valid_registration_data2['email']
        ).first()
        assert user1 is not None
        assert user2 is not None


# Test user registration with same email
def test_signup_email_in_use():
    client = app.test_client()
    client.delete('/clear')
    response1 = client.post(
        'auth/signup',
        data=valid_registration_data1,
        follow_redirects=True
    )
    assert response1.status_code == 200
    response2 = client.post(
        '/auth/signup',
        data=valid_registration_data1,
        follow_redirects=True
    )
    assert response2.status_code == 400
    message = json.loads(response2.data)
    assert message['error'] == 'Email is already in use'


# Test user registration with non matching passwords
def test_signup_password_not_matching():
    client = app.test_client()
    client.delete('/clear')
    invalid_data = valid_registration_data1.copy()
    invalid_data['confirmPassword'] = 'val0dPassword'
    response = client.post(
        '/auth/signup',
        data=invalid_data,
        follow_redirects=True
    )
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Passwords do not match'


# Test user registration with long first name
def test_signup_long_first_name():
    client = app.test_client()
    client.delete('/clear')
    invalid_data = valid_registration_data1.copy()
    invalid_data['firstName'] = 'a' * 16
    response = client.post(
        '/auth/signup',
        data=invalid_data,
        follow_redirects=True
    )
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'First name cannot exceed 15 characters'


# Test user registration with empty first name
def test_signup_first_name_empty():
    client = app.test_client()
    client.delete('/clear')
    invalid_data = valid_registration_data1.copy()
    invalid_data['firstName'] = ''
    response = client.post(
        '/auth/signup',
        data=invalid_data,
        follow_redirects=True
    )
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'First name cannot be empty'


# Test user registration with long last name
def test_signup_last_name_too_long():
    client = app.test_client()
    client.delete('/clear')
    invalid_data = valid_registration_data1.copy()
    invalid_data['lastName'] = 'a' * 16
    response = client.post(
        '/auth/signup',
        data=invalid_data,
        follow_redirects=True
    )
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Last name cannot exceed 15 characters'


# Test user registration with empty last name
def test_signup_last_name_empty():
    client = app.test_client()
    client.delete('/clear')
    invalid_data = valid_registration_data1.copy()
    invalid_data['lastName'] = ''
    response = client.post(
        '/auth/signup',
        data=invalid_data,
        follow_redirects=True
    )
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Last name cannot be empty'


# Test user registration with invalid email
def test_signup_invalid_email():
    client = app.test_client()
    client.delete('/clear')
    invalid_data = valid_registration_data1.copy()
    invalid_data['email'] = 'example.com'
    response = client.post(
        '/auth/signup',
        data=invalid_data,
        follow_redirects=True
    )
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Email must be of a valid format'


# Test user registration with short password
def test_signup_password_too_short():
    client = app.test_client()
    client.delete('/clear')
    invalid_data = valid_registration_data1.copy()
    invalid_data['password'] = 'a1'
    invalid_data['confirmPassword'] = 'a1'
    response = client.post(
        '/auth/signup',
        data=invalid_data,
        follow_redirects=True
    )
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Password should be atleast 8 characters'


# Test user registration with long password
def test_signup_password_too_long():
    client = app.test_client()
    client.delete('/clear')
    invalid_data = valid_registration_data1.copy()
    invalid_data['password'] = 'a1' * 8
    invalid_data['confirmPassword'] = 'a1' * 8
    response = client.post(
        '/auth/signup',
        data=invalid_data,
        follow_redirects=True
    )
    assert response.status_code == 400
    message = json.loads(response.data)
    assert (message['error'] ==
            'Password shouldn\'t exceed 15 characters')


# Test user registration with password not containing numbers
def test_signup_password_does_not_contain_number():
    client = app.test_client()
    client.delete('/clear')
    invalid_data = valid_registration_data1.copy()
    invalid_data['password'] = 'p' * 9
    invalid_data['confirmPassword'] = 'p' * 9
    response = client.post(
        '/auth/signup',
        data=invalid_data,
        follow_redirects=True
    )
    assert response.status_code == 400
    message = json.loads(response.data)
    assert (message['error'] ==
            'Password should contain atleast one letter and one number')


# Test user registration with password not containing letters
def test_signup_password_does_not_contain_letter():
    client = app.test_client()
    client.delete('/clear')
    invalid_data = valid_registration_data1.copy()
    invalid_data['password'] = '1' * 9
    invalid_data['confirmPassword'] = '1' * 9
    response = client.post(
        '/auth/signup',
        data=invalid_data,
        follow_redirects=True
    )
    assert response.status_code == 400
    message = json.loads(response.data)
    assert (message['error'] ==
            'Password should contain atleast one letter and one number')

# ================================================
# ======== Test Cases for the login route ========
# ================================================


# Test successful login
def test_login_successful():
    client = app.test_client()
    client.delete('/clear')
    client.post(
        '/auth/signup',
        data=valid_registration_data1,
        follow_redirects=True
    )
    response = client.post(
        '/auth/login',
        data=valid_login_data,
        follow_redirects=True
    )
    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(
            email=valid_registration_data1['email']
        ).first()
        assert user is not None
        token = Token.query.filter_by(user_id=user.id).first()
        assert token is not None


# Test login with incorrect password
def test_login_incorrect_password():
    client = app.test_client()
    client.delete('/clear')
    client.post(
        '/auth/signup',
        data=valid_registration_data1,
        follow_redirects=True
    )
    invalid_data = valid_login_data.copy()
    invalid_data['password'] = 'p0sswords'
    response = client.post(
        '/auth/login',
        data=invalid_data,
        follow_redirects=True
    )
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Invalid email and/or password'


# Test login for user that doesn't exist
def test_login_user_does_not_exist():
    client = app.test_client()
    client.delete('/clear')
    response = client.post(
        '/auth/login',
        data=valid_login_data,
        follow_redirects=True
    )
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Invalid email and/or password'

# ================================================
# ======= Test Cases for the logout route ========
# ================================================


# Test successfull logout
def test_logout_success():
    client = app.test_client()
    client.delete('/clear')
    client.post(
        '/auth/signup',
        data=valid_registration_data1,
        follow_redirects=True
    )
    client.post('/auth/login', data=valid_login_data, follow_redirects=True)
    response1 = client.get('/auth/logout', follow_redirects=True)
    assert response1.status_code == 200
    response2 = client.get('/mailbox', follow_redirects=True)
    assert response2.status_code == 400
    message = json.loads(response2.data)
    assert message['error'] == 'Invalid userId'


# Test successfull logout when not logged in
def test_logout_when_not_logged_in_success():
    client = app.test_client()
    client.delete('/clear')
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
