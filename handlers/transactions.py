from flask import app, make_response, redirect, render_template, request, send_from_directory
import web
import services

@web.register("/changeBalance", methods=['POST'])
def handle_transaction(auth):
    recipient = request.form.get("recipient")
    amount = request.form.get("amount")
    # Either pay or request
    transactionType = request.form.get("transactionType")
    description = request.form.get("description")

    services.transaction.perform_transaction(auth["uid"], recipient, amount, description, transactionType == "pay")

    return redirect("/dashboard")
