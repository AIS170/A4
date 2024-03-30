from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from .models import User, Invoice, CommunicationReport
import os
import json
from datetime import datetime
from .database import db
from xml.etree import ElementTree as ET
from datetime import datetime

reports = Blueprint('report_mailbox', __name__)

@reports.route('', methods=['GET'])
def reportBox():
    user_id_a = session.get('user_id')
    if not user_id_a:
        return jsonify({'error': 'Invalid userId'}), 400
    communication_reports = CommunicationReport.query.filter_by(user_id=user_id_a).all()
    formatted_reports = []
    for report in communication_reports:
        invoice = Invoice.query.filter_by(id=report.invoice_id).first()
        new_report = {
            'id': report.id,
            'details': report.details,
            'date_reported': report.date_reported,
            'invoice_subject': invoice.subject if invoice else None
        }
        formatted_reports.append(new_report)
    return formatted_reports