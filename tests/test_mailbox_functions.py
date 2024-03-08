import pytest
import uuid
import requests
import json
import random

BASE_URL = "http://localhost:5000"

from A4.src.mailbox import (
    show_mailbox,
    incomingInvoiceId,
    incomingLookup,
    sending,
    sent,
    sentInvoiceId,
    sentLookup,
    sentReportId,
    verifySent,
    deleteIncomingInvoice,
    deleteSentInvoice
)



def test_mailbox_invalid_userId():

    invalid_userId = "!!invalid!!"  
    response = requests.get(f"{BASE_URL}/mailbox/mailbox", params={"userId": invalid_userId})
    
    assert response.status_code == 400
    assert 'Invalid userId' in response.json().get('error', '')

    print(f"Invalid userId test passed with response code {response.status_code} and message: {response.json()}")



def test_incoming_invoice_invalid_id():

    params = {
        "userId": "validUserId",
        "incomingInvoiceId": "invalid"  # This should trigger a validation error
    }
    response = requests.get(f"{BASE_URL}/mailbox/mailbox/incomingInvoice/", params=params)
    
    assert response.status_code == 400
    assert 'Invalid incomingInvoiceId.' in response.json().get('error', '')

    print(f"Test for invalid incomingInvoiceId passed with response code {response.status_code} and message: {response.json()}")


def test_incoming_invoice_unauthorized_access():

    response = requests.get(f"{BASE_URL}/mailbox/mailbox/incomingInvoice/", params={
        "userId": 321,
        "incomingInvoiceId": "123"
    })
    
    assert response.status_code == 401
    assert 'User is not a recipient of this Invoice.' in response.json().get('error', '')

    print("Unauthorized access test passed with 401 response code and message:", response.json())


# def test_valid_user_invoice():
    
#     response = requests.get(f"{BASE_URL}/mailbox/mailbox/incomingInvoice/", params={
#         "userId": 420,
#         "incomingInvoiceId": "123"
#     })

#     assert response.status_code == 200
#     # assert 'User is not a recipient of this Invoice.' in response.json().get('error', '')

#     print("Unauthorized access test passed with 401 response code and message:", response.json())


def test_fail_on_sending_with_no_invoice():
    # Example of sending a request with no e-invoices attached
    data = {
        "userId": 320,
        "recipientAddresses": ["recipient@example.com"],
        "invoiceSubject": "Valid Subject",
        "invoiceBody": "Valid Body",
        "eInvoices": []  # No e-invoices attached
    }
    response = requests.post(f"{BASE_URL}/mailbox/mailbox/sending/", json=data, )
    assert response.status_code == 400
    assert 'No e-invoice attached' in response.json()['error']
    print("no e-invoice attached test passed with 400 resp and msg", response.json())


def test_fail_on_excess_sub_char_limit():
    # Example of sending a request with excess subj char limit.
    data = {
        "userId": 320,
        "recipientAddresses": ["recipient@example.com"],
        "invoiceSubject": "Hello world, Hello world, Hello world, Hello world, Hello world, Hello world",
        "invoiceBody": "Valid Body",
        "eInvoices": ['invoice_1']
    }
    response = requests.post(f"{BASE_URL}/mailbox/mailbox/sending/", json=data, )
    assert response.status_code == 400
    assert 'Invoice subject exceeds character limit.' in response.json()['error']
    print("Invoice subject excess character limit test passed with 400 resp and msg", response.json())


def test_fail_on_excess_body_char_limit():
    # Example of sending a request with no body char limit exceeded.

    data = {
        "userId": 320,
        "recipientAddresses": ["recipient@example.com"],
        "invoiceSubject": "Hello world",
        "invoiceBody": "body - This is a test to check if the character limit of the mail has exceeded. This is a test script.",
        "eInvoices": ['invoice_1']
    }
    response = requests.post(f"{BASE_URL}/mailbox/mailbox/sending/", json=data, )
    assert response.status_code == 400
    assert 'Invoice body exceeds character limit.' in response.json()['error']
    print("Invoice body excess character limit test passed with 400 resp and msg", response.json())


def test_fail_on_receiptients_not_exists():
    # Example of sending a request with no body char limit exceeded.

    data = {
        "userId": 320,
        "recipientAddresses": ["mail21@abc.com"],
        "invoiceSubject": "Hello world",
        "invoiceBody": "body - within limits",
        "eInvoices": ['invoice_1']
    }
    response = requests.post(f"{BASE_URL}/mailbox/mailbox/sending/", json=data, )
    assert response.status_code == 404
    assert 'One or more recipients do not exist.' in response.json()['error']
    print("invalid receiptient test passed with 404 resp and msg", response.json())




# def test_sucess_sending():
#     # Example of sending a request with no e-invoices attached
#     data = {
#         "userId": 320,
#         "recipientAddresses": ["recipient@example.com"],
#         "invoiceSubject": "Valid Subject",
#         "invoiceBody": "Valid Body",
#         "eInvoices": ['a']  # No e-invoices attached
#     }
#     response = requests.post(f"{BASE_URL}/mailbox/mailbox/sending/", json=data, )
#     assert response.status_code == 200
#     # assert 'No e-invoice attached' in response.json()['error']
