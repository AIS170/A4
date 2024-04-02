import pytest
import sys
import os
import json
from io import BytesIO
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from src.models import User, Token, Invoice, CommunicationReport

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