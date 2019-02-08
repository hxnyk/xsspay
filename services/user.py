import db

def get_user(user_id):
    with db.connect() as cursor:
        cursor.execute("SELECT username, balance from users where id = %s", (user_id,))
        return cursor.fetchone()
    
    return None
