import pytest
import sys
import os
import json
from io import BytesIO
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from backend.src.models import User

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

valid_login_data1 = {
    "email": "user@example.com",
    "password": "val1dPassword",
}

valid_login_data2 = {
    "email": "user2@example.com",
    "password": "val1dPassword",
}

valid_sent_email_data1 = {
    "recipient_address": "user2@example.com",
    "invoice_subject": "New mail",
    "invoice_file": 'data.xml',
}

valid_sent_email_data2 = {
    "recipient_address": "user@example.com",
    "invoice_subject": "New mail",
    "invoice_file": 'data.xml',
}

# ================================================
# ==== Test Cases for the User Details route =====
# ================================================

# Test successfully view user details
def test_user_details_success():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)

    response = client.get('/user/details', follow_redirects=True)
    assert response.status_code == 200

# Test user details not logged in
def test_user_details_invalid_user_id():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)

    response = client.get('/user/details', follow_redirects=True)
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Invalid userId'

# ================================================
# ==== Test Cases for the Change Email route =====
# ================================================
    
# Test email changed successfully
def test_email_change_success():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)

    response = client.put('/user/email', data={'new_email': "newemail@newemail.com"}, follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(email="newemail@newemail.com").first()
        assert user is not None
    
# Test email change not logged in
def test_email_change_invalid_user_id():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)

    response = client.put('/user/email', data={'new_email': "newemail@newemail.com"}, follow_redirects=True)
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Invalid userId'

# Test email change invalid email format
def test_email_change_invalid_email():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)

    response = client.put('/user/email', data={'new_email': "newemail.com"}, follow_redirects=True)
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Email must be of a valid format'

# Test email change new email same as current email
def test_email_change_new_email_same_as_current_email():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)

    response = client.put('/user/email', data={'new_email': "user@example.com"}, follow_redirects=True)
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'New email is the same as current email'

# Test email change new email already in use
def test_email_change_email_in_use():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)
    client.get('/auth/logout', follow_redirects=True)
    client.post('/auth/signup', data=valid_registration_data2, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data2, follow_redirects=True)

    response = client.put('/user/email', data={'new_email': "user@example.com"}, follow_redirects=True)
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Email is already in use'

# ================================================
# === Test Cases for the Change Password route ===
# ================================================
    
# Test password changed successfully
def test_password_change_success():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)

    response = client.put('/user/password', data={'new_password': "str0ngPass"}, follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(password="str0ngPass").first()
        assert user is not None
    
# Test password change not logged in
def test_password_change_invalid_user_id():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)

    response = client.put('/user/password', data={'new_password': "str0ngPass"}, follow_redirects=True)
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Invalid userId'

# Test password change password too short
def test_password_change_password_too_short():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)

    response = client.put('/user/password', data={'new_password': "str0ng"}, follow_redirects=True)
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Password should be atleast 8 characters'

# Test password change password too long
def test_password_change_password_too_long():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)

    response = client.put('/user/password', data={'new_password': "str0ngPassworddd"}, follow_redirects=True)
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Password shouldn\'t exceed 15 characters'

# Test password change password doesn't contain atleast one letter
def test_password_change_password_no_letters():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)

    response = client.put('/user/password', data={'new_password': "000000000"}, follow_redirects=True)
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Password should contain atleast one letter and one number'

# Test password change password doesn't contain atleast one number
def test_password_change_password_no_numbers():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)

    response = client.put('/user/password', data={'new_password': "aaaaaaaaa"}, follow_redirects=True)
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Password should contain atleast one letter and one number'