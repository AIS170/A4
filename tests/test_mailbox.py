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

@pytest.fixture
def session():
    return requests.Session()

#Test successfully send mail
def test_sending_to_self_success(session):
    session.delete(f"{BASE_URL}/clear")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data1)
    session.get(f"{BASE_URL}/auth/logout")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data2)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data2)

    response = session.post(f"{BASE_URL}/mailbox/sending", data=valid_sent_email_data1, files={'invoice_file': open('tests/data.xml', 'rb')})
    assert response.status_code == 200

def test_sending_success(session):
    session.delete(f"{BASE_URL}/clear")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data1)
    session.get(f"{BASE_URL}/auth/logout")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data2)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data2)

    response = session.post(f"{BASE_URL}/mailbox/sending", data=valid_sent_email_data2, files={'invoice_file': open('tests/data.xml', 'rb')})
    assert response.status_code == 200
    session.delete(f"{BASE_URL}/clear")

def test_sending_multiple_mail_success(session):
    session.delete(f"{BASE_URL}/clear")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data1)
    session.get(f"{BASE_URL}/auth/logout")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data2)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data2)

    response = session.post(f"{BASE_URL}/mailbox/sending", data=valid_sent_email_data1, files={'invoice_file': open('tests/data.xml', 'rb')})
    assert response.status_code == 200
    response = session.post(f"{BASE_URL}/mailbox/sending", data=valid_sent_email_data2, files={'invoice_file': open('tests/data.xml', 'rb')})
    assert response.status_code == 200

def test_sending_invalid_user(session):
    session.delete(f"{BASE_URL}/clear")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data1)
    session.get(f"{BASE_URL}/auth/logout")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data2)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data2)

    session.get(f"{BASE_URL}/auth/logout")
    response = session.post(f"{BASE_URL}/mailbox/sending", data=valid_sent_email_data1, files={'invoice_file': open('tests/data.xml', 'rb')})
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Invalid userId'

def test_sending_invalid_recipient(session):
    session.delete(f"{BASE_URL}/clear")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data1)
    session.get(f"{BASE_URL}/auth/logout")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data2)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data2)

    invalid_data = valid_sent_email_data1.copy()
    invalid_data['recipient_address'] = 'invalid@example.com'
    response = session.post(f"{BASE_URL}/mailbox/sending", data=invalid_data, files={'invoice_file': open('tests/data.xml', 'rb')})
    message = response.json()
    assert message['error'] == 'Recipient does not exist'
    assert response.status_code == 404

def test_sending_empty_subject(session):
    session.delete(f"{BASE_URL}/clear")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data1)
    session.get(f"{BASE_URL}/auth/logout")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data2)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data2)

    invalid_data = valid_sent_email_data1.copy()
    invalid_data['invoice_subject'] = ''
    response = session.post(f"{BASE_URL}/mailbox/sending", data=invalid_data, files={'invoice_file': open('tests/data.xml', 'rb')})
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Subject cannot be empty'

def test_sending_subject_too_long(session):
    session.delete(f"{BASE_URL}/clear")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data1)
    session.get(f"{BASE_URL}/auth/logout")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data2)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data2)

    invalid_data = valid_sent_email_data1.copy()
    invalid_data['invoice_subject'] = 'a' * 51
    response = session.post(f"{BASE_URL}/mailbox/sending", data=invalid_data, files={'invoice_file': open('tests/data.xml', 'rb')})
    assert response.status_code == 400
    message = response.json()
    assert message['error'] == 'Subject cannot be over 50 characters long'

def test_mailbox_success(session):
    session.delete(f"{BASE_URL}/clear")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data1)
    session.get(f"{BASE_URL}/auth/logout")
    session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data2)
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data2)

    session.post(f"{BASE_URL}/mailbox/sending", data=valid_sent_email_data2, files={'invoice_file': open('tests/data.xml', 'rb')})
    session.get(f"{BASE_URL}/auth/logout")
    session.post(f"{BASE_URL}/auth/login", data=valid_login_data1)
    response = session.get(f"{BASE_URL}/mailbox")
    assert response.status_code == 200

# def test_mailbox_success_multiple_mails(session):
#     session.delete(f"{BASE_URL}/clear")
#     session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
#     session.post(f"{BASE_URL}/auth/login", data=valid_login_data1)
#     session.get(f"{BASE_URL}/auth/logout")
#     session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data2)
#     session.post(f"{BASE_URL}/auth/login", data=valid_login_data2)

#     session.post(f"{BASE_URL}/mailbox/sending", data=valid_sent_email_data2, files={'invoice_file': open('tests/data.xml', 'rb')})
#     mail2 = valid_sent_email_data1.copy()
#     mail2['invoice_subject'] = 'Another one'
#     session.post(f"{BASE_URL}/mailbox/sending", data=mail2, files={'invoice_file': open('tests/data.xml', 'rb')})
#     session.get(f"{BASE_URL}/auth/logout")
#     session.post(f"{BASE_URL}/auth/login", data=valid_login_data1)
#     response = session.get(f"{BASE_URL}/mailbox")
#     assert response.status_code == 200

# def test_mailbox_inavlid_user(session):
#     session.delete(f"{BASE_URL}/clear")
#     session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data1)
#     session.post(f"{BASE_URL}/auth/login", data=valid_login_data1)
#     session.get(f"{BASE_URL}/auth/logout")
#     session.post(f"{BASE_URL}/auth/signup", data=valid_registration_data2)
#     session.post(f"{BASE_URL}/auth/login", data=valid_login_data2)

#     session.get(f"{BASE_URL}/auth/logout")
#     response = session.get(f"{BASE_URL}/mailbox")
#     assert response.status_code == 400