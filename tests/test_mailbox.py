import pytest
import sys
import os
import json
from io import BytesIO
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db
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

# Test successfully send mail to self
def test_sending_to_self_success():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)
    client.get('/auth/logout', follow_redirects=True)
    client.post('/auth/signup', data=valid_registration_data2, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data2, follow_redirects=True)

    with open('tests/data.xml', 'rb') as file:
        valid_file_content = BytesIO(file.read())
    valid_data = valid_sent_email_data1.copy()
    valid_data['invoice_file'] = (valid_file_content, 'data.xml')
    response = client.post('/mailbox/sending', data=valid_data, follow_redirects=True)
    assert response.status_code == 200

# Test successfully send mail to another user
def test_sending_success():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)
    client.get('/auth/logout', follow_redirects=True)
    client.post('/auth/signup', data=valid_registration_data2, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data2, follow_redirects=True)

    with open('tests/data.xml', 'rb') as file:
        valid_file_content = BytesIO(file.read())
    valid_data = valid_sent_email_data2.copy()
    valid_data['invoice_file'] = (valid_file_content, 'data.xml')
    response = client.post('/mailbox/sending', data=valid_data, follow_redirects=True)
    assert response.status_code == 200
    client.delete('/clear')

# Test successfully send multiple mail
def test_sending_multiple_mail_success():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)
    client.get('/auth/logout', follow_redirects=True)
    client.post('/auth/signup', data=valid_registration_data2, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data2, follow_redirects=True)

    with open('tests/data.xml', 'rb') as file:
        valid_file_content = BytesIO(file.read())
    valid_data = valid_sent_email_data1.copy()
    valid_data['invoice_file'] = (valid_file_content, 'data.xml')
    response = client.post('/mailbox/sending', data=valid_data, follow_redirects=True)
    assert response.status_code == 200

    with open('tests/data.xml', 'rb') as file:
        valid_file_content = BytesIO(file.read())
    valid_data2 = valid_sent_email_data2.copy()
    valid_data2['invoice_file'] = (valid_file_content, 'data.xml')

    response = client.post('/mailbox/sending', data=valid_data2, follow_redirects=True)
    assert response.status_code == 200

# Test send mail with invalid userId
def test_sending_invalid_user():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)
    client.get('/auth/logout', follow_redirects=True)
    client.post('/auth/signup', data=valid_registration_data2, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data2, follow_redirects=True)

    with open('tests/data.xml', 'rb') as file:
        valid_file_content = BytesIO(file.read())
    valid_data = valid_sent_email_data1.copy()
    valid_data['invoice_file'] = (valid_file_content, 'data.xml')

    client.get('/auth/logout', follow_redirects=True)
    response = client.post('/mailbox/sending', data=valid_data, follow_redirects=True)
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Invalid userId'

# Test send mail to non-existent user
def test_sending_invalid_recipient():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)
    client.get('/auth/logout', follow_redirects=True)
    client.post('/auth/signup', data=valid_registration_data2, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data2, follow_redirects=True)

    invalid_data = valid_sent_email_data1.copy()
    invalid_data['recipient_address'] = 'invalid@example.com'
    with open('tests/data.xml', 'rb') as file:
        valid_file_content = BytesIO(file.read())
    invalid_data['invoice_file'] = (valid_file_content, 'data.xml')

    response = client.post('/mailbox/sending', data=invalid_data, follow_redirects=True)
    message = json.loads(response.data)
    assert message['error'] == 'Recipient does not exist'
    assert response.status_code == 404

# Test send mail with empty subject
def test_sending_empty_subject():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)
    client.get('/auth/logout', follow_redirects=True)
    client.post('/auth/signup', data=valid_registration_data2, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data2, follow_redirects=True)

    invalid_data = valid_sent_email_data1.copy()
    invalid_data['invoice_subject'] = ''
    with open('tests/data.xml', 'rb') as file:
        valid_file_content = BytesIO(file.read())
    invalid_data['invoice_file'] = (valid_file_content, 'data.xml')

    response = client.post('/mailbox/sending', data=invalid_data, follow_redirects=True)
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Subject cannot be empty'

# Test send mail with subject over 50 characters long
def test_sending_subject_too_long():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)
    client.get('/auth/logout', follow_redirects=True)
    client.post('/auth/signup', data=valid_registration_data2, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data2, follow_redirects=True)

    invalid_data = valid_sent_email_data1.copy()
    invalid_data['invoice_subject'] = 'a' * 51
    with open('tests/data.xml', 'rb') as file:
        valid_file_content = BytesIO(file.read())
    invalid_data['invoice_file'] = (valid_file_content, 'data.xml')

    response = client.post('/mailbox/sending', data=invalid_data, follow_redirects=True)
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Subject cannot be over 50 characters long'

# Test send mail with invalid file
def test_sending_invalid_file():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)
    client.get('/auth/logout', follow_redirects=True)
    client.post('/auth/signup', data=valid_registration_data2, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data2, follow_redirects=True)

    invalid_data = valid_sent_email_data1.copy()
    with open('tests/invalid.txt', 'rb') as file:
        valid_file_content = BytesIO(file.read())
    invalid_data['invoice_file'] = (valid_file_content, 'invalid.txt')

    response = client.post('/mailbox/sending', data=invalid_data, follow_redirects=True)
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message['error'] == 'Invalid Invoice'


#Test deleted invoice succesfully 
def test_delete_invoice_success():
    client = app.test_client()
    client.delete('/clear')
    client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data1, follow_redirects=True)
    
    client.get('/auth/logout', follow_redirects=True)
    client.post('/auth/signup', data=valid_registration_data2, follow_redirects=True)
    client.post('/auth/login', data=valid_login_data2, follow_redirects=True)

    with open('tests/data.xml', 'rb') as file:
        valid_file_content = file.read()
    
    
    valid_data = valid_sent_email_data2.copy()
    valid_data['invoice_file'] = (BytesIO(valid_file_content), 'data.xml')
    client.post('/mailbox/sending', data=valid_data, follow_redirects=True)
    
    
    with app.app_context():
        latest_invoice = Invoice.query.order_by(Invoice.id.desc()).first()
        assert latest_invoice is not None, "Failed to create invoice"
        invoice_id = latest_invoice.id

    
        delete_response = client.delete(f'/mailbox/{invoice_id}/delete', follow_redirects=True)
        assert delete_response.status_code == 200, "Invoice should be successfully deleted."

    
        deleted_invoice = Invoice.query.get(invoice_id)
        assert deleted_invoice is None, "Invoice was not successfully deleted."




# Test delete invoice with invalid userId
def test_delete_invoice_invalid_user(client):

    some_invoice_id = "someinvoiceid"

    delete_response = client.delete(f'/mailbox/{some_invoice_id}/delete')
    

    assert delete_response.status_code == 400








# Test successfully view mailbox after sending mail
# def test_mailbox_success():
#     client = app.test_client()
#     client.delete('/clear')
#     client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
#     client.post('/auth/login', data=valid_login_data1, follow_redirects=True)
#     client.get('/auth/logout', follow_redirects=True)
#     client.post('/auth/signup', data=valid_registration_data2, follow_redirects=True)
#     client.post('/auth/login', data=valid_login_data2, follow_redirects=True)

#     client.post('/mailbox/sending', data=valid_sent_email_data2, follow_redirects=True)
#     client.get('/auth/logout', follow_redirects=True)
#     client.post('/auth/login', data=valid_login_data1, follow_redirects=True)
#     response = client.get('/mailbox', follow_redirects=True)
#     assert response.status_code == 200

# Test successfully view mailbox after sending multiple mail
# def test_mailbox_success_multiple_mails():
#     client = app.test_client()
#     client.delete('/clear')
#     client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
#     client.post('/auth/login', data=valid_login_data1, follow_redirects=True)
#     client.get('/auth/logout', follow_redirects=True)
#     client.post('/auth/signup', data=valid_registration_data2, follow_redirects=True)
#     client.post('/auth/login', data=valid_login_data2, follow_redirects=True)

#     client.post('/mailbox/sending', data=valid_sent_email_data2)
#     mail2 = valid_sent_email_data1.copy()
#     mail2['invoice_subject'] = 'Another one'
#     client.post('/mailbox/sending', data=mail2, follow_redirects=True)
#     client.get('/auth/logout', follow_redirects=True)
#     client.post('/auth/login', data=valid_login_data1, follow_redirects=True)
#     response = client.get('/mailbox')
#     assert response.status_code == 200

# Test view mailbox with invalid userId
# def test_mailbox_inavlid_user():
#     client = app.test_client()
#     client.delete('/clear')
#     client.post('/auth/signup', data=valid_registration_data1, follow_redirects=True)
#     client.post('/auth/login', data=valid_login_data1, follow_redirects=True)
#     client.get('/auth/logout', follow_redirects=True)
#     client.post('/auth/signup', data=valid_registration_data2, follow_redirects=True)
#     client.post('/auth/login', data=valid_login_data2, follow_redirects=True)

#     client.get('/auth/logout', follow_redirects=True)
#     response = client.get('/mailbox', follow_redirects=True)
#     assert response.status_code == 400