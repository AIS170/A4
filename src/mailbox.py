from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

mailbox = Blueprint('mailbox_route', __name__)
# View all received/incoming e-invoices for specified user through userId. Returns senderAddress, timeSent and invoiceSubject
@mailbox.route('', methods=['GET'])
def mailBox():
    user_id = request.args.get('user_id')
    return render_template('mailbox.html')


# View received e-invoice through userId and incomingInvoiceId, returns list that contains senderAddress, timeSent, invoiceSubject, 
# invoiceBody, list of eInvoices containing name, content, timeCreated and owner.
def incomingInvoiceId(userId, incomingInvoiceId):

    return list



# Sends e-invoice to desired recepient given userId, recepientAddress, invoiceSubject, 
# invoiceBody and list of eInvoices containing name, content, timeCreated and owner. Returns list for sentReport containing content
# and sentReportId.
def sending(userId, recepientAdresses, invoiceSubject, invoiceBody, eInvoices):

    return list


# View outgoing sent e-invoices given userId, returns recepientAddres, timeSent and invoiceSubject.
def sent(userId):

    return list


# View sent e-invoice through userId and sentInvoiceId, returns list that contains recepientAddress, timeSent, invoiceSubject, 
# invoiceBody, list of eInvoices containing name, content, timeCreated and owner, and sendReport list which contains content and sentReportId.
def sentInvoiceId(userId, sentInvoiceId):

    return list



  

# View report for sent e-invoice given userId, sentInvoiceId and sentReportId. Returns sentReport list containing content and sentReportId.
def sentReportId(userId: str, sentInvoiceId: int, sentReportId: int):

    return list








