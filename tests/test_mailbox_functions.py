import pytest

from mailbox import (
    mailBox,
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

def test_mailBox_empty():
    result = mailBox('user1')
    assert result == []

def test_mailBox_with_received_invoices(): # Assuming the mailbox has invoices
    result = mailBox('user1')
    assert isinstance(result, list)
    assert len(result) > 0
    
def test_mailBox_invalid_userId():
    with pytest.raises(ValueError) as exc_info:
        mailBox('')
    
    assert str(exc_info.value) == "User ID cannot be empty"

def test_mailBox_nonexistent_user():
    result = mailBox('no_user')
    assert result == "User does not exist"

def test_mailBox_non_string_userId():
    with pytest.raises(ValueError) as exc_info:
        mailBox(123)
    
    assert str(exc_info.value) == "User ID must be a string"




def test_incomingInvoiceId_empty():
    result = incomingInvoiceId('user1', 1)
    assert result == []

def test_incomingLookup_empty():
    result = incomingLookup('user1', 'lookup_string')
    assert result == []

def test_sending_successful():
    e_invoices = [
        {'name': 'item1', 'content': 'description1', 'timeCreated': '2024-03-05', 'owner': 'user1'},
        {'name': 'item2', 'content': 'description2', 'timeCreated': '2024-03-05', 'owner': 'user1'}
    ]
    result = sending('user1', ['user1@doimanname.com'], 'Invoice Subject', 'Invoice Body', e_invoices)
    assert isinstance(result, list)
    assert 'content' in result[0]
    assert 'sentReportId' in result[0]



def test_sent_empty():
    result = sent('user1')
    assert result == []




def test_sentInvoiceId_empty():
    result = sentInvoiceId('user1', 1)
    assert result == []




def test_sentLookup_empty():
    result = sentLookup('user1', 'lookup_string')
    assert result == []




def test_sentReportId_empty():
    result = sentReportId('user1', 1, 1)
    assert result == []




def test_verifySent_empty():
    result = verifySent('user1', 1)
    assert result == []



def test_deleteIncomingInvoice_successful():
    result = deleteIncomingInvoice('user1', 1)
    assert result is None



def test_deleteSentInvoice_successful():
    result = deleteSentInvoice('user1', 1)
    assert result is None
