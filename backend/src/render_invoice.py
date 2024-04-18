import io
from flask import (Blueprint, render_template, request, send_file, jsonify,
                   session)
import requests


render_invoice = Blueprint('render_invoice', __name__)


def register_user():
    data = {
        'email': 'A4@gmail.com',
        'password': 'yoA4',
        'first_name': 'A4Ecom',
        'last_name': 'A4Ecomme'
    }
    response = requests.post(
        "http://rendering.ap-southeast-2.elasticbeanstalk.com/pages/register",
        data=data
    )
    return response.status_code == 200


def login_user():
    data = {'email': 'A4@gmail.com', 'password': 'yoA4'}
    response = requests.post(
        "http://rendering.ap-southeast-2.elasticbeanstalk.com/pages/login",
        data=data
    )
    if response.status_code == 200:
        token = response.json().get('token')
        return token
    return None


@render_invoice.route('/', methods=['GET', 'POST'])
def render_invoice_function():
    # Register user on external API (you need to implement this)
    register_user()

    # Login user to obtain token from external API (you need to implement this)
    login_user()

    # Check if user is logged in (you need to implement this)
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    if request.method == 'POST':
        # Extract form data from the request
        form_data = request.form

        try:
            # Make request to external API to create the invoice
            response1 = requests.post(
                "http://rendering.ap-southeast-2.elasticbeanstalk.com/render",
                data=form_data
            )
            print(response1)
            if response1.status_code == 200:
                # Determine the output type selected by the user
                output_type = form_data.get('outputType')
                content_type = ''
                file_extension = ''
                if output_type == 'HTML':
                    content_type = 'text/html'
                    file_extension = 'html'
                elif output_type == 'PDF':
                    content_type = 'application/pdf'
                    file_extension = 'pdf'
                elif output_type == 'JSON':
                    content_type = 'application/json'
                    file_extension = 'json'

                # Send the rendered invoice file for download
                return send_file(
                    io.BytesIO(response1),
                    mimetype=content_type,
                    as_attachment=True,
                    attachment_filename=f"invoice.{file_extension}"
                )

        except requests.exceptions.RequestException as e:
            # Handle exceptions if any
            return jsonify({"error": str(e)})

    return render_template('rendering.html')
