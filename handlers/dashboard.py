from flask import app, render_template, request
import web
import services

@web.register("/dashboard")
def getDashboard(auth):
    user = services.user.get_user(auth["uid"])
    name = user["username"]
    balance = user["balance"]
    return render_template('dashboard.html', username=name, balance=balance)

@web.register("/account")
def getAccount(auth):
    return render_template('account.html')

@web.register("/history")
def getHistory(auth):
    query = request.args.get("query")
    transactions = services.transaction.get_readable_transactions_for_user(auth["uid"])
    balance = services.user.get_user(auth["uid"])["balance"]
    return render_template('history.html', transactions=transactions, balance=balance, query=query)

@web.register("/transactions")
def getTransactions(auth):
    balance = services.user.get_user(auth["uid"])["balance"]
    return render_template('transactions.html', balance=balance)
