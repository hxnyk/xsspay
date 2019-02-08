@web.register("/dashboard")
def getDashboard():
    return render_template('dashboard.html')

@web.register("/account")
def getAccount():
    return render_template('account.html')

@web.register("/history")
def getHistory():
    return render_template('history.html')

@web.register("/transactions")
def getTransactions():
    return render_template('transactions.html')

@web.register("/logout")
def logout():
    return render_template('auth.html')
