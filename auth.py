import db
import time

from flask import request, Response

AUTH_COOKIE = "xps"


def web(func):
    def inner_wrapper(*args, **kwargs):
        def grab_auth():
            if AUTH_COOKIE in request.cookies:
                token = request.cookies.get(AUTH_COOKIE)

                # fetch session, verify expiration, grab uid
                auth = get_uid_from_session(token)
                return auth
            return None

        if "auth" in func.__code__.co_varnames:
            auth = grab_auth()

            if not auth:
                return Response("Unauthorized", 401)
            return func(auth=auth, *args, **kwargs)
        else if "op_auth" in func.__code__.co_varnames:
            auth = grab_auth()
            return func(op_auth=auth, *args, **kwargs)

        return func(*args, **kwargs)
    
    # Set wrapper name to wrapped function for flask mapping
    inner_wrapper.__name__ = func.__name__
    return inner_wrapper


def get_uid_from_session(token):
    with db.connect() as cursor:
        # In pymysql %s is how they express `?` for prepared statements. It's sanitized.
        cursor.execute("SELECT uid FROM sessions WHERE token = %s AND expire > %s", (token, int(time.time())))

        result = cursor.fetchone()

        return result["uid"] if result else None
