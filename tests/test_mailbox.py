import pytest
import requests

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
}

valid_sent_email_data2 = {
    "recipient_address": "user@example.com",
    "invoice_subject": "New mail",
}

files = {'invoice_file': open('tests/data.xml', 'rb')}

@pytest.fixture(autouse=True)
def setup():
    requests.delete(f"{BASE_URL}/clear")
    requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    requests.post(f"{BASE_URL}/auth/login", data=valid_login_data1)
    requests.post(f"{BASE_URL}/auth/logout")
    requests.post(f"{BASE_URL}/auth/signup", data=valid_registration_data2)
    requests.post(f"{BASE_URL}/auth/login", data=valid_login_data2)

#Test successfully send mail
def test_sending_success():
    response = requests.post(f"{BASE_URL}/mailbox/sending", data=valid_sent_email_data2, files=files)
    assert response.status_code == 400, 200
    
def test_sending_to_self_success():
    response = requests.post(f"{BASE_URL}/mailbox/sending", data=valid_sent_email_data1, files=files)
    assert response.status_code == 400, 200

def test_sending_multiple_mail_success():
    response = requests.post(f"{BASE_URL}/mailbox/sending", data=valid_sent_email_data1, files=files)
    assert response.status_code == 400, 200
    response = requests.post(f"{BASE_URL}/mailbox/sending", data=valid_sent_email_data2, files=files)
    assert response.status_code == 400, 200

def test_sending_invalid_user():
    requests.post(f"{BASE_URL}/auth/logout")
    response = requests.post(f"{BASE_URL}/mailbox/sending", data=valid_sent_email_data1, files=files)
    assert response.status_code == 400

def test_sending_invalid_recipient():
    invalid_data = valid_sent_email_data1.copy()
    invalid_data['recipient_address'] = 'invalid@example.com'
    response = requests.post(f"{BASE_URL}/mailbox/sending", data=invalid_data, files=files)
    assert response.status_code == 400

def test_sending_empty_subject():
    invalid_data = valid_sent_email_data1.copy()
    invalid_data['invoice_subject'] = ''
    response = requests.post(f"{BASE_URL}/mailbox/sending", data=invalid_data, files=files)
    assert response.status_code == 400

def test_sending_subject_too_long():
    invalid_data = valid_sent_email_data1.copy()
    invalid_data['invoice_subject'] = 'a' * 51
    response = requests.post(f"{BASE_URL}/mailbox/sending", data=invalid_data, files=files)
    assert response.status_code == 400

def test_mailbox_success():
    requests.post(f"{BASE_URL}/mailbox/sending", data=valid_sent_email_data2, files=files)
    requests.post(f"{BASE_URL}/auth/logout")
    requests.post(f"{BASE_URL}/auth/login", data=valid_login_data1)
    response = requests.get(f"{BASE_URL}/mailbox")
    assert response.status_code == 400, 200

def test_mailbox_success_multiple_mails():
    requests.post(f"{BASE_URL}/mailbox/sending", data=valid_sent_email_data2, files=files)
    mail2 = valid_sent_email_data1.copy()
    mail2['invoice_subject'] = 'Another one'
    requests.post(f"{BASE_URL}/mailbox/sending", data=mail2, files=files)
    requests.post(f"{BASE_URL}/auth/logout")
    requests.post(f"{BASE_URL}/auth/login", data=valid_login_data1)
    response = requests.get(f"{BASE_URL}/mailbox")
    assert response.status_code == 400, 200

def test_mailbox_inavlid_user():
    requests.post(f"{BASE_URL}/auth/logout")
    response = requests.get(f"{BASE_URL}/mailbox")
    assert response.status_code == 400