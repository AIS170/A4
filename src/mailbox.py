from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from .models import User, Invoice, CommunicationReport
import os
import xmltodict, json
from datetime import datetime
from .database import db
from xml.etree import ElementTree as ET

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
        user_id_a = session.get('user_id')
        recipient_address = request.form.get('recipient_address')
        invoice_subject = request.form.get('invoice_subject')
        # invoice_body = request.form.get('invoice_body')
        auth_user = User.query.filter_by(id=user_id_a)

        if auth_user is None:
            return jsonify({'error': 'Invalid user ID'}), 400
        recipient = User.query.filter_by(email=recipient_address).first()
        if recipient is None:
            return jsonify({'error': 'Recipient does not exist'}), 404
        if invoice_subject == None:
            return jsonify({'error': 'Subject cannot be null'}), 400
        if len(invoice_subject) > 50:
            return jsonify({'error': 'Subject cannot be over 50 characters long'}), 400
        # if invoice_body == None:
        #     return jsonify({'error': 'Body cannot be null'}), 400
        # elif len(invoice_body) > 1000:
        #     return jsonify({'error': 'Body cannot be over 1000 characters long'}), 400
        
        xml_file = request.files.get('invoice_file')
        if xml_file and allowed_file(xml_file.filename):
            xml_content = xml_file.read()
            invoice_dict = xml_to_dict(xml_content)
            invoice_json = json.dumps(invoice_dict)
            
            new_mail = Invoice(id=os.urandom(24).hex(), subject=invoice_subject, body=invoice_json, date_sent=datetime.now(), user_id=user_id_a, is_incoming=False, sent_to_user_id=recipient.id)
            db.session.add(new_mail)
            db.session.commit()

            report_details = "Invoice Sent Details:\nSubject: {}\nRecipient: \nSender: {}\nDate Sent: {}".format(invoice_subject, recipient_address, user_id_a, datetime.now())
            new_comm_report = CommunicationReport(id=os.urandom(24).hex(), invoice_id=new_mail.id, details=report_details, date_reported=datetime.now())
            db.session.add(new_comm_report)
            db.session.commit()
            return redirect(url_for('mailbox_route.mailBox'))
        else: 
            return jsonify({'error': 'Invalid Invoice'}), 400
    return render_template('send.html')


# def helperConvert(file):
#     o = xmltodict.parse('<e> <a>text</a> <a>text</a> </e>')
#     json.dumps(o)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xml'}


def xml_to_dict(xml_content):
    root = ET.fromstring(xml_content)
    return {child.tag: child.text for child in root}

    