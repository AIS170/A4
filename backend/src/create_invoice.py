from flask import (Blueprint, render_template, request, redirect, url_for,
                   jsonify)
import requests


create_invoice = Blueprint('create_invoice', __name__)


# Calls an external API to create a valid XML invoice
@create_invoice.route('/create/', methods=['GET', 'POST'])
def invoice_create():
    if request.method == 'POST':
        form_data = request.form

        # Assuming the external API routes
        gui_route = "https://ubl-invoice-generator.vercel.app/invoices/guest" \
            "/gui"
        download_route = "https://ubl-invoice-generator.vercel.app/invoices/" \
                         "guest/file/download"

        try:
            # Make request to external API to create the invoice
            gui_response = requests.post(gui_route, data=form_data)

            if gui_response.status_code == 200:
                # Optionally handle success response
                # Make request to download the invoice
                download_response = requests.get(
                    download_route,
                    data=form_data
                )

                if download_response.status_code == 200:
                    # Optionally handle success response for download
                    return redirect(url_for('download_invoice'))
                else:
                    # Optionally handle error response for download
                    return jsonify({"error": "Failed to download invoice"})
            else:
                # Optionally handle error response for invoice creation
                return jsonify({"error": "Failed to create invoice"})
        except requests.exceptions.RequestException as e:
            # Handle exceptions if any
            return jsonify({"error": str(e)})
    return render_template('external_api.html')
