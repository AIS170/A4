from flask import Blueprint, jsonify, render_template, session
import json

from backend.src.mailbox import xml_to_dict
from backend.src.models import User, Invoice
from backend.src.database import db

from datetime import datetime


tracking = Blueprint('tracking', __name__)

def calculate_user_financials_and_history(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return None, None, "User not found"

    total_credit = 0.0
    total_debit = 0.0
    transactions = []
    running_balance = 0.0  # Initialize the running balance
    invoice_counter = 1

    # Process invoices
    for invoice in user.sent_invoices + user.received_invoices:
        invoice_data = xml_to_dict(invoice.body)
        if invoice_data:
            amount = float(invoice_data.get('tax_inclusive_amount', 0))
            
            # Check if the invoice is sent or received
            if invoice in user.sent_invoices:
                total_debit += amount
                running_balance += amount  # Deduct the amount from the running balance
                description = 'Invoice Received'
            else:
                total_credit += amount
                running_balance -= amount  # Add the amount to the running balance
                description = 'Invoice Sent'
            
            # Retrieve and format invoice number
            # invoice_number = invoice_data.get('invoice_number', 'N/A')
            
            # Append transaction details
            transactions.append({
                'invoice_number': invoice_counter,
                'description': description,
                'debit': amount if invoice in user.received_invoices else 0.0,
                'credit': amount if invoice in user.sent_invoices else 0.0,
                'balance': running_balance
            })
            invoice_counter += 1


    financial_summary = {
        'total_credit': total_credit,
        'total_debit': total_debit,
        'net_balance': total_credit - total_debit
    }

    return financial_summary, transactions, None
    

@tracking.route('/', methods=['GET'])
def get_financials():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    financial_data, transactions, error = calculate_user_financials_and_history(user_id)
    if error:
        return jsonify({'error': error}), 404
    else:
        return render_template('tracking.html', financials=financial_data, transactions=transactions, user_id=user_id)