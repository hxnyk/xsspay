from flask import app, render_template
import services
import web

@web.register("/dashboard")
def getDashboard(auth):
    context = services.user.get_user(auth['uid'])
    return render_template('dashboard.html', **context)

@web.register("/account")
def getAccount(auth):
    context = services.user.get_user(auth['uid'])
    return render_template('account.html', **context)

@web.register("/history")
def getHistory(auth):
    context = services.user.get_user(auth['uid'])
    return render_template('history.html', **context)

@web.register("/transactions")
def getTransactions(auth):
    context = services.user.get_user(auth['uid'])
    return render_template('transactions.html', **context)
