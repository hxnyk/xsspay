import bcrypt
import db
import secrets
import time

SESSION_LENGTH = 3600
TOKEN_LENGTH = 16

def signup_user(username, password):
    encoded_password = password.encode('utf-8')
    
    if len(encoded_password) > 72:
        return None
    
    if len(username) < 3:
        return None
    
    with db.connect() as cursor:
        # In pymysql %s is how they express `?` for prepared statements. It's sanitized.
        cursor.execute("SELECT username as count FROM users WHERE username = %s", (username.lower(),))

        result = cursor.fetchone()

        # user exists
        if result:
            return None
        
        password_hash = bcrypt.hashpw(encoded_password, bcrypt.gensalt())

        cursor.execute("INSERT INTO users (username, password, balance) VALUES (%s, %s, %s)", (username.lower(), password_hash, 100.00))

        cursor.execute("SELECT id from users where username = %s", (username.lower(),))

        result = cursor.fetchone()

        return result["id"]

def login_user(username, password):
    encoded_password = password.encode('utf-8')
    
    if len(encoded_password) > 72:
        return None
    
    with db.connect() as cursor:
        cursor.execute("SELECT id, password from users where username = %s", (username.lower(),))

        result = cursor.fetchone()

        if not result:
            return None
        
        uid = result["id"]
        stored_password = result["password"]

        if bcrypt.checkpw(encoded_password, stored_password.encode('utf-8')):
            # authenticated :D
            expiration = int(time.time()) + SESSION_LENGTH
            token = secrets.token_hex(TOKEN_LENGTH)

            cursor.execute("INSERT INTO sessions (uid, token, expire) VALUES (%s, %s, %s)", (uid, token, expiration))

            return token

        return None

def logout_user(session):
    with db.connect() as cursor:
        cursor.execute("DELETE FROM sessions WHERE token = %s", (session,))
