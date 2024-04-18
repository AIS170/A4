from flask import (Blueprint, render_template, request, redirect, url_for,
                   jsonify, session)
from backend.src.models import User, Invoice, CommunicationReport
import os
from backend.src.database import db
from xml.etree import ElementTree as ET
from datetime import datetime

mailbox = Blueprint('mailbox_route', __name__)


# Retrieves the current users received mails
@mailbox.route('', methods=['GET'])
def mailBox():
    user_id_a = session.get('user_id')
    if not user_id_a:
        return jsonify({'error': 'Invalid userId'}), 400

    user = User.query.filter_by(id=user_id_a).first()

    # Retrieve search query parameters
    search_subject = request.args.get('subject', '')
    search_sender_address = request.args.get('sender_address', '')

    search_invoice_id = request.args.get('invoice_id', '')

    # Start with a base query
    received_mails_query = Invoice.query.join(
        User,
        Invoice.user_id == User.id
    ).filter(
        Invoice.sent_to_user_id == user_id_a
    )

    # Apply filters based on search criteria
    if search_subject:
        received_mails_query = received_mails_query.filter(
            Invoice.subject.ilike(f'%{search_subject}%')
        )
    if search_sender_address:
        received_mails_query = received_mails_query.filter(
            User.email.ilike(f'%{search_sender_address}%')
        )

    if search_invoice_id:
        received_mails_query = received_mails_query.filter(
            Invoice.id == search_invoice_id
        )

    # Execute the query
    received_mails = received_mails_query.all()

    current_datetime = datetime.now()

    formatted_mail = []
    for mail in received_mails:
        user = User.query.filter_by(id=mail.user_id).first()
        new_mail = {
            'id': mail.id,
            'subject': mail.subject,
            'body': mail.body,
            'date_sent': mail.date_sent,
            'user_id': mail.user_id,
            'read': mail.read,
            'sender_mail': user.email
        }
        formatted_mail.append(new_mail)

    for i in received_mails:
        if i.read:
            continue
        else:
            i.read = True
            sender = User.query.filter_by(id=i.user_id).first()
            recipient = User.query.filter_by(id=i.sent_to_user_id).first()
            report_details = ("Invoice Received Details:\n"
                              "Subject: {}\n"
                              "Recipient: {}\n"
                              "Sender: {}\n"
                              "Date Received: {}").format(
                                i.subject,
                                recipient.email,
                                sender.email,
                                datetime.now()
                              )
            new_comm_report = CommunicationReport(
                id=os.urandom(24).hex(),
                invoice_id=i.id,
                user_id=user_id_a,
                details=report_details,
                date_reported=datetime.now()
            )
            db.session.add(new_comm_report)
            db.session.commit()

    return render_template(
        'mailbox.html',
        received_mails=formatted_mail,
        current_datetime=current_datetime,
        search_subject=search_subject,
        search_sender_address=search_sender_address,
        # user_first_name=user.first_name,
        # user_last_name=user.last_name
    )


# Sends e-invoice to desired recepient given userId, recepientAddress,
# invoiceSubject, invoiceBody and list of eInvoices containing name, content,
# timeCreated and owner. Returns list for sentReport containing content and
# sentReportId.
@mailbox.route('/sending', methods=['GET', 'POST'])
def sending():

    if request.method == 'POST':
        user_id_a = session.get('user_id')
        if user_id_a is None:
            return jsonify({'error': 'Invalid userId'}), 400

        recipient_addresses_raw = request.form.get('recipient_addresses')
        invoice_subject = request.form.get('invoice_subject')
        # user = User.query.filter_by(id=user_id_a).first()

        # recipient = User.query.filter_by(email=recipient_addresses_raw)
        # .first()
        # the user
        sender = User.query.filter_by(id=user_id_a).first()

        # if recipient == None:
        #     return jsonify({'error': 'Recipient does not exist'}), 404
        if invoice_subject == '':
            return jsonify({'error': 'Subject cannot be empty'}), 400
        if len(invoice_subject) > 50:
            return jsonify(
                {'error': 'Subject cannot be over 50 characters long'}
            ), 400

        files = request.files.getlist('invoice_files[]')
        if not files or any(not allowed_file(file.filename) for file in files):
            return jsonify({'error': 'Invalid Invoice file(s)'}), 400

        recipient_emails = [
            email.strip() for email in recipient_addresses_raw.split(' ')
        ]
        valid_recipients = []
        invalid_emails = []

        for email in recipient_emails:
            recipient = User.query.filter_by(email=email).first()
            if recipient:
                valid_recipients.append(recipient)
            else:
                invalid_emails.append(email)

        if invalid_emails:
            return (
                jsonify({
                    'error': 'Some recipient emails are invalid: ' +
                             ', '.join(invalid_emails)
                }),
                404
            )

        for recipient in valid_recipients:
            for file in files:

                # reset file pointer to 0 when reading body for other
                # recipient(s)
                file.seek(0)
                xml_content = file.read()
                invoice_dict = xml_to_dict(xml_content)
                if invoice_dict is None:
                    return (
                        jsonify({
                            'error': f"Failed to parse XML content in file "
                                     f"{file.filename}"}), 400
                    )

                new_mail = Invoice(
                    id=os.urandom(24).hex(),
                    subject=invoice_subject,
                    body=xml_content,
                    date_sent=datetime.now(),
                    user_id=user_id_a,
                    read=False,
                    sent_to_user_id=recipient.id
                )
                db.session.add(new_mail)

                report_details = (
                    "Invoice Sent Details:\n"
                    "Subject: {}\n"
                    "Recipient: {}\n"
                    "Sender: {}\n"
                    "Date Sent: {}"
                ).format(
                    invoice_subject,
                    recipient_addresses_raw,
                    sender.email,
                    datetime.now()
                )
                new_comm_report = CommunicationReport(
                    id=os.urandom(24).hex(),
                    invoice_id=new_mail.id,
                    user_id=user_id_a,
                    details=report_details,
                    date_reported=datetime.now()
                )
                db.session.add(new_comm_report)

        db.session.commit()
        return redirect(url_for('mailbox_route.mailBox'))
    return render_template('send.html')


# Helper function to check if a file is valid
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xml'}


# Helper functionto convert xml to a json dictionary
def xml_to_dict(xml_content):
    if not xml_content.strip():
        return {}
    try:
        root = ET.fromstring(xml_content)
        ns = {
            'cac': ('urn:oasis:names:specification:ubl:schema:xsd:'
                    'CommonAggregateComponents-2'),
            'cbc': ('urn:oasis:names:specification:ubl:schema:xsd:'
                    'CommonBasicComponents-2')
        }

        # Extract relevant data
        tax_amount = root.find('.//cac:TaxTotal/cbc:TaxAmount', ns).text
        tax_exclusive_amount = root.find(
            './/cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount',
            ns
        ).text
        tax_inclusive_amount = root.find(
            './/cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount',
            ns
        ).text

        return {
            'tax_amount': tax_amount,
            'tax_exclusive_amount': tax_exclusive_amount,
            'tax_inclusive_amount': tax_inclusive_amount
        }
    except ET.ParseError as e:
        print("An error occurred while parsing XML: ", e)
        return None


# Provides detailed information on a specified invoice
@mailbox.route('/<string:invoiceId>', methods=['GET'])
def invoiceShow(invoiceId):
    user_id_a = session.get('user_id')
    if user_id_a is None:
        return jsonify({'error': 'Invalid userId'}), 400
    invoice = Invoice.query.filter_by(id=invoiceId).first()
    if invoice:
        # Assuming you want to render a template with details of the invoice
        return render_template('invoice.html', invoice=invoice)
    else:
        return jsonify({'error': 'Invoice not found'}), 404


# Deletes a specified invoice from the database
@mailbox.route('/<string:invoiceId>/delete', methods=['GET', 'DELETE'])
def delete_invoice(invoiceId):
    if request.method == 'DELETE':
        user_id_a = session.get('user_id')
        invoice = Invoice.query.filter_by(id=invoiceId).first()

        if not user_id_a:
            return jsonify({'error': 'Invalid userId'}), 400

        if not invoice:
            return jsonify({'error': 'Invoice does not exist'}), 404

        db.session.delete(invoice)
        db.session.commit()
        return redirect(url_for('mailbox_route.mailBox'))
    else:
        return jsonify({'error': 'Method Not Allowed'}), 405
