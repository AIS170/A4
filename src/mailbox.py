from flask import Blueprint, render_template, request, redirect, url_for, jsonify

mailbox = Blueprint('mailbox', __name__)

@mailbox.route('/mailbox/', methods=['GET'])
# View all received/incoming e-invoices for specified user through userId. Returns senderAddress, timeSent and invoiceSubject
def mailBox():
    userId = request.args.get('userId')
    
    if not userId or not userId.isalnum():  
        return jsonify({'error': 'Invalid userId'}), 400
    
    # Simulate fetching data for the valid userId (replace with actual data fetching logic)
    incoming_previews = [
        {"senderAddress": "sender@example.com", "timeSent": 123456789, "invoiceSubject": "Invoice #123"},
        {"senderAddress": "another@example.com", "timeSent": 987654321, "invoiceSubject": "Invoice #456"}
    ]
    
    return jsonify(incoming_previews), 200



# View received e-invoice through userId and incomingInvoiceId, returns list that contains senderAddress, timeSent, invoiceSubject, 
# invoiceBody, list of eInvoices containing name, content, timeCreated and owner.
@mailbox.route('/mailbox/incomingInvoice/', methods=['GET'])
def incomingInvoiceId():
    user_id = request.args.get('userId')
    incoming_invoice_id = request.args.get('incomingInvoiceId')
    
    
    if not user_id or not incoming_invoice_id:
        return jsonify({'error': 'Invalid request parameters'}), 400

    
    try:
        incoming_invoice_id = int(incoming_invoice_id)
    except ValueError:
        return jsonify({'error': 'Invalid incomingInvoiceId.'}), 400

    
    authorized = True  
    if not authorized:
        return jsonify({'error': 'User is not a recipient of this Invoice.'}), 401
    
    
    incoming_invoice = {
        "senderAddress": "sender@example.com",
        "timeSent": 123456789,
        "invoiceSubject": "Invoice #123",
        "invoiceBody": "This is an example invoice body.",
        "e-invoices": ["file1.pdf", "file2.pdf"]
    }
    
    return jsonify(incoming_invoice), 200




# Lookup e-invoice in mailbox using lookupString and userId, returns list that contains senderAdress, timeSent and invoiceSubject.
def incomingLookup(userId: str, lookupString: str) -> list or str:

    return list


# Sends e-invoice to desired recepient given userId, recepientAddress, invoiceSubject, 
# invoiceBody and list of eInvoices containing name, content, timeCreated and owner. Returns list for sentReport containing content
# and sentReportId.
def sending(userId: str, recepientAdresses: list, invoiceSubject: str, invoiceBody: str, eInvoices: list) -> list or str:

    return list


# View outgoing sent e-invoices given userId, returns recepientAddres, timeSent and invoiceSubject.
def sent(userId: str) -> list or str:

    return list


# View sent e-invoice through userId and sentInvoiceId, returns list that contains recepientAddress, timeSent, invoiceSubject, 
# invoiceBody, list of eInvoices containing name, content, timeCreated and owner, and sendReport list which contains content and sentReportId.
def sentInvoiceId(userId: str, sentInvoiceId: int) -> list or str:

    return list


# Lookup e-invoice in mailbox using lookupString and userId, returns list that contains recepientAdress, timeSent and invoiceSubject.
def sentLookup(userId: str, lookupString: str) -> list or str:

    return list
  

# View report for sent e-invoice given userId, sentInvoiceId and sentReportId. Returns sentReport list containing content and sentReportId.
def sentReportId(userId: str, sentInvoiceId: int, sentReportId: int) -> list or str:

    return list


# verifies sent e-invoice given userId and sentInvoiceId. Returns deliveryStatusReport list containing content and deliveryStatusReportId.
def verifySent(userId: str, sentInvoiceId: int) -> list or str:

    return list


# Deletes received e-inovice given userId and incomingIncoiveId. Returns nothing.
def deleteIncomingInvoice(userId: str, incomingInvoiceId: int) -> None or str:

    return None


# Deletes sent e-inovice given userId and sentIncoiveId. Returns nothing.
def deleteSentInvoice(userId: str, sentInvoiceId: int) -> None or str:

    return None
