import services
import web

from flask import app, make_response, redirect, render_template, request, send_from_directory
from flask import Flask

SIGNUP_FLAG = "signup"
LOGIN_FLAG = "login"

@web.register("/")
def index_handler_get():
    return render_template('auth.html')

@web.register("/", methods=['POST'])
def index_handler_post():
    # determine if sign up
    if "signup" in request.form:
        services.auth.signup_user(request.form.get("username"), request.form.get("password"))
        
        return redirect("/")
    else:
        # do auth
        session = services.auth.login_user(request.form.get("username"), request.form.get("password"))

        if session:
            # cookie here
            response = redirect("/dashboard")
            response.set_cookie(web.AUTH_COOKIE, session)

            return response
        
        return redirect("/")
