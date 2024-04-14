from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from .models import User, Invoice, CommunicationReport
import os
import json
from datetime import datetime
from .database import db
from xml.etree import ElementTree as ET
from datetime import datetime

reports = Blueprint('reports', __name__)

@reports.route('', methods=['GET'])
def reportBox():
    user_id_a = session.get('user_id')
    if not user_id_a:
        return jsonify({'error': 'Invalid userId'}), 400

    
    search_sender = request.args.get('sender')
    search_subject = request.args.get('subject')
    search_invoice_id = request.args.get('invoice_id')

    
    query = CommunicationReport.query.filter(CommunicationReport.user_id == user_id_a)

    
    if search_sender:
        
        query = query.join(CommunicationReport.invoice).join(Invoice.sender).filter(User.first_name.ilike(f"%{search_sender}%") | User.last_name.ilike(f"%{search_sender}%"))
    if search_subject:
        
        query = query.join(CommunicationReport.invoice).filter(Invoice.subject.ilike(f"%{search_subject}%"))
    if search_invoice_id:
        query = query.filter(CommunicationReport.invoice_id == search_invoice_id)

    
    communication_reports = query.all()

    user = User.query.filter_by(id=user_id_a).first()
    formatted_reports = []

    for report in communication_reports:
        new_report = {
            'id': report.id,
            'details': report.details,
            'date_reported': report.date_reported,
            'invoice_subject': report.invoice.subject,
            }
        formatted_reports.append(new_report)
    
    return render_template('report.html', formatted_reports=formatted_reports, user=user)
