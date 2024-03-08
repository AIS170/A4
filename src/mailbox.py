from flask import Blueprint, render_template, request, redirect, url_for, jsonify
# All functions may also be subject to return error message
mailbox = Blueprint('mailbox', __name__)

# View all received/incoming e-invoices for specified user through userId. Returns senderAddress, timeSent and invoiceSubject

@mailbox.route('/', methods=['GET'])
def mailBox():
    user_id = request.args.get('user_id')
    return '[incomingPreviews]'


# View received e-invoice through userId and incomingInvoiceId, returns list that contains senderAddress, timeSent, invoiceSubject, 
# invoiceBody, list of eInvoices containing name, content, timeCreated and owner.
@mailbox.route('/<int:incomingInvoiceId>', methods=['GET'])
def incomingInvoiceId(incomingInvoiceId):
    user_id = request.args.get('user_id')
    return 'incomingInvoice'


# Lookup e-invoice in mailbox using lookupString and userId, returns list that contains senderAdress, timeSent and invoiceSubject.
@mailbox.route('/mailbox/lookup', methods=['GET'])
def incomingLookup():
    user_id = request.args.get('user_id')
    lookup = request.form.get('lookup_string')
    return '[incomingPreviews]'


# Sends e-invoice to desired recepient given userId, recepientAddress, invoiceSubject, 
# invoiceBody and list of eInvoices containing name, content, timeCreated and owner. Returns list for sentReport containing content
# and sentReportId.
@mailbox.route('/mailbox/sending', methods=['GET', 'POST'])
def sending():
    if request.method == 'POST':
        user_id = request.args.get('user_id')
        recepient_address = request.form.get('recepient_address')
        invoice_subject = request.form.get('invoice_subject')
        invoice_body = request.form.get('invoice_body')
        e_invoices = request.form.get('e_invoices')
        return 'sentReport'
    return None


# View outgoing sent e-invoices given userId, returns recepientAddres, timeSent and invoiceSubject.
@mailbox.route('/mailbox/sent', methods=['GET'])
def sent():
    user_id = request.args.get('user_id')
    return 'sentPreview'


# View sent e-invoice through userId and sentInvoiceId, returns list that contains recepientAddress, timeSent, invoiceSubject, 
# invoiceBody, list of eInvoices containing name, content, timeCreated and owner, and sendReport list which contains content and sentReportId.
@mailbox.route('/mailbox/sent/<int:sentInvoiceId>', methods=['GET'])
def sentInvoiceId(sentInvoiceId):
    user_id = request.args.get('user_id')

    return 'sentInvoice, sentReport'


# Lookup e-invoice in mailbox using lookupString and userId, returns list that contains recepientAdress, timeSent and invoiceSubject.
@mailbox.route('/mailbox/sent/lookup', methods=['GET'])
def sentLookup():
    user_id = request.args.get('user_id')
    lookup = request.form.get('lookup_string')
    return 'sentPreview'
  

# View report for sent e-invoice given userId, sentInvoiceId and sentReportId. Returns sentReport list containing content and sentReportId.
@mailbox.route('/mailbox/sent/<int:sent_invoice_id>/<int:sent_report_id>', methods=['GET'])
def sentReportId(sentInvoiceId, sentReportId):
    user_id = request.args.get('user_id')
    return list


# verifies sent e-invoice given userId and sentInvoiceId. Returns deliveryStatusReport list containing content and deliveryStatusReportId.
@mailbox.route('/mailbox/sent/<int:sent_invoice_id>/verify_sent', methods=['GET'])
def verifySent(sentInvoiceId):
    user_id = request.args.get('user_id')
    return list


# Deletes received e-inovice given userId and incomingIncoiveId. Returns nothing.
@mailbox.route('/mailbox/sent/<int:incoming_invoice_id>/delete', methods=['GET'])
def deleteIncomingInvoice(incomingInvoiceId):
    user_id = request.args.get('user_id')
    return None


# # Deletes sent e-inovice given userId and sentIncoiveId. Returns nothing.
# @mailbox.route('/mailbox/sent/<int=sent_invoice_id>/delete')
# def deleteSentInvoice(sentInvoiceId):
#     user_id = request.args.get('user_id')
#     return None
