from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from .models import User, Invoice
import os
import xmltodict, json
from datetime import datetime
from .database import db
mailbox = Blueprint('mailbox_route', __name__)
# View all received/incoming e-invoices for specified user through userId. Returns senderAddress, timeSent and invoiceSubject
@mailbox.route('', methods=['GET'])
def mailBox():
    user_id = request.args.get('user_id')
    return render_template('mailbox.html')


@mailbox.route('/<string:invoiceId>', methods=['GET'])
def invoiceId():

    return list

@mailbox.route('/<string:reportId>', methods=['GET'])
def reportId():
    return list

# Sends e-invoice to desired recepient given userId, recepientAddress, invoiceSubject, 
# invoiceBody and list of eInvoices containing name, content, timeCreated and owner. Returns list for sentReport containing content
# and sentReportId.
@mailbox.route('/sending', methods=['GET', 'POST'])
def sending():
    if request.method == 'POST':
        user_id = session.get('user_id')
        recipient_address = request.form.get('recipient_address')
        invoice_subject = request.form.get('invoice_subject')
        invoice_body = request.form.get('invoice_body')
        auth_user = User.query.filter_by(id=user_id)
        if auth_user is None:
            return jsonify({'error': 'Invalid user ID'}), 400
        recipient = User.query.filter_by(email=recipient_address).first()
        if recipient is None:
            return jsonify({'error': 'Recipient does not exist'}), 404
        if invoice_subject == None:
            return jsonify({'error': 'Subject cannot be null'}), 400
        if len(invoice_subject) > 50:
            return jsonify({'error': 'Subject cannot be over 50 characters long'}), 400
        if invoice_body == None:
            return jsonify({'error': 'Body cannot be null'}), 400
        elif len(invoice_body) > 1000:
            return jsonify({'error': 'Body cannot be over 1000 characters long'}), 400
        
        new_mail = Invoice(id=os.urandom(24).hex(), subject=invoice_subject, body=invoice_body, date_sent=datetime.now(), user_id=user_id, is_incoming=False, sent_to_user_id=recipient.id)
        db.session.add(new_mail)
        db.session.commit()

        return redirect(url_for('mailbox_route.mailBox'))
    return render_template('send.html')


def helperConvert(file):
    o = xmltodict.parse('<e> <a>text</a> <a>text</a> </e>')
    json.dumps(o)






