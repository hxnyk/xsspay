from flask import app, make_response, redirect, render_template, request, send_from_directory
import web

@web.register("/changeBalance", methods=['POST'])
def handle_transaction():
    recipient = request.form.get("recipient")
    amount = request.form.get("amount")
    # Either pay or request
    transactionType = request.form.get("transactionType")

    return render_template('dashboard.html')