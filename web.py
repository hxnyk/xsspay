import db
import time

from flask import Flask, request, Response

AUTH_ARG = "auth"
AUTH_COOKIE = "xps"

def register(path, methods=['GET']):
    def inner_web(func):
        def inner_wrapper(*args, **kwargs):
            if AUTH_ARG in func.__code__.co_varnames:
                # Get the variables name of the function -- (auth, a, b) or (a, b, auth=None)
                # Flip the order -- (b, a, auth) or (auth=None, b, a)
                # Find the index of AUTH_ARG -- 2 or 0
                auth_index = func.__code__.co_varnames[::-1].index(AUTH_ARG)

                # Check if auth has a default value set -- (2 < 0) or (0 < 1)
                is_strict_auth = not auth_index < len(func.__defaults__)

                auth = grab_auth()

                if is_strict_auth and not auth:
                    return Response("Unauthorized", 401)
                return func(auth=auth, *args, **kwargs)
            return func(*args, **kwargs)
        
        # Set wrapper name to wrapped function for flask mapping
        inner_wrapper.__name__ = func.__name__
        app.route(path, methods=methods)(inner_wrapper)

        return inner_wrapper
    return inner_web


def get_uid_from_session(token):
    with db.connect() as cursor:
        # In pymysql %s is how they express `?` for prepared statements. It's sanitized.
        cursor.execute("SELECT uid FROM sessions WHERE token = %s AND expire > %s", (token, int(time.time())))

        result = cursor.fetchone()

        return result["uid"] if result else None

def grab_auth():
    if AUTH_COOKIE in request.cookies:
        token = request.cookies.get(AUTH_COOKIE)

        # fetch session, verify expiration, grab uid
        auth = get_uid_from_session(token)
        return auth
    return None