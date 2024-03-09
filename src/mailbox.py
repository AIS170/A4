from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

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

        return redirect(url_for('mailbox_route.mailBox'))
    return render_template('send.html')









