from flask import Blueprint, render_template, request, jsonify, session
from .models import Invoice, CommunicationReport

reports = Blueprint('reports', __name__)


@reports.route('', methods=['GET'])
def reportBox():
    user_id_a = session.get('user_id')
    if not user_id_a:
        return jsonify({'error': 'Invalid userId'}), 400

    search_subject = request.args.get('subject')
    search_invoice_id = request.args.get('invoice_id')

    query = CommunicationReport.query.filter(
        CommunicationReport.user_id == user_id_a
    )

    if search_subject:
        query = query.filter(
            CommunicationReport.invoice.has(
                Invoice.subject.ilike(f"%{search_subject}%")
            )
        )
    if search_invoice_id:
        query = query.filter(
            CommunicationReport.invoice_id == search_invoice_id
        )

    communication_reports = query.all()

    formatted_reports = []

    print(communication_reports)

    # Check if communication_reports is not empty
    if communication_reports:
        for report in communication_reports:
            if (report.invoice):
                new_report = {
                    'id': report.id,
                    'details': report.details,
                    'date_reported': report.date_reported,
                    'invoice_subject': report.invoice.subject,
                }
                formatted_reports.append(new_report)
            else:
                continue

    if not formatted_reports:
        return render_template(
            'report.html',
            formatted_reports=None,
            reports_empty=True
        )
    else:
        return render_template(
            'report.html',
            formatted_reports=formatted_reports,
            reports_empty=False
        )
