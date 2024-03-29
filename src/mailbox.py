from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from .models import User, Invoice, CommunicationReport
import os
import json
from datetime import datetime
from .database import db
from xml.etree import ElementTree as ET
from datetime import datetime

mailbox = Blueprint('mailbox_route', __name__)
# View all received/incoming e-invoices for specified user through userId. Returns senderAddress, timeSent and invoiceSubject
@mailbox.route('', methods=['GET'])
def mailBox():
    user_id_a = session.get('user_id')
    if not user_id_a:
        return jsonify({'error': 'Invalid userId'}), 400
    
    received_mails = Invoice.query.filter_by(sent_to_user_id=user_id_a).all()

    current_datetime = datetime.now()

    formatted_mail = []
    for mail in received_mails:
        user = User.query.filter_by(id=mail.sent_to_user_id).first()
        new_mail = {
            'id': mail.id,
            'subject': mail.subject,
            'body': mail.body,
            'date_sent': mail.date_sent,
            'user_id': mail.user_id,
            'is_incoming': mail.is_incoming,
            'sent_to_user_mail': user.email
        }
        formatted_mail.append(new_mail)

    for i in received_mails:
        report_details = "Invoice Sent Details:\nSubject: {}\nRecipient: \nSender: {}\nDate Sent: {}".format(i.subject, i.sent_to_user_id, user_id_a, datetime.now())
        new_comm_report = CommunicationReport(id=os.urandom(24).hex(), invoice_id=i.id, details=report_details, date_reported=datetime.now())
        db.session.add(new_comm_report)
        db.session.commit()
    
    return render_template('mailbox.html', received_mails=formatted_mail, current_datetime=current_datetime)


# @mailbox.route('/<string:invoiceId>', methods=['GET'])
# def invoiceId():

#     return list

# @mailbox.route('/<string:reportId>', methods=['GET'])
# def reportId():
#     return list

# Sends e-invoice to desired recepient given userId, recepientAddress, invoiceSubject, 
# invoiceBody and list of eInvoices containing name, content, timeCreated and owner. Returns list for sentReport containing content
# and sentReportId.
@mailbox.route('/sending', methods=['GET', 'POST'])
def sending():
    if request.method == 'POST':
        user_id_a = session.get('user_id')
        if user_id_a == None:
            return jsonify({'error': 'Invalid userId'}), 400
        recipient_address = request.form.get('recipient_address')
        invoice_subject = request.form.get('invoice_subject')
        # invoice_body = request.form.get('invoice_body')   
        recipient = User.query.filter_by(email=recipient_address).first()
        if recipient == None:
            return jsonify({'error': 'Recipient does not exist'}), 404
        if invoice_subject == '':
            return jsonify({'error': 'Subject cannot be empty'}), 400
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


# Helper function to check if a file is valid
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xml'}

# Helper function to convert XML content into a Python dictionary
def xml_to_dict(xml_content):
    root = ET.fromstring(xml_content)
    return {child.tag: child.text for child in root}


@mailbox.route('/<string:invoiceId>', methods=['GET'])
def invoiceShow(invoiceId):
    invoice = Invoice.query.get(invoiceId)
    if invoice:
        # Assuming you want to render a template with the details of the invoice
        return render_template('invoice.html', invoice=invoice)
    else:
        return jsonify({'error': 'Invoice not found'}), 404
    

@mailbox.route('/<string:invoiceId>/delete', methods=['DELETE'])
def delete_invoice(invoiceId):
    user_id_a = session.get('user_id')
    invoice = Invoice.query.get(invoiceId)
    # checks here
    if not user_id_a:
        return jsonify({'error': 'Invalid userId'}), 400
    
    if not invoice:
        return jsonify({'error': 'Invoice does not exist'}), 404
    
    if invoice.user_id != user_id_a:
        return jsonify({'error': 'You are not authorized to delete this invoice'}), 403

    db.session.delete(invoice)
    db.session.commit()
    return redirect(url_for('mailbox_route.mailBox'))