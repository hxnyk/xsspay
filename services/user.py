import db

def get_username(user_id):
    with db.connect() as cursor:
        cursor.execute("SELECT username from users where id = %s"(user_id,))

        result = cursor.fetchone()

        return result["username"] if result else None
    
    return None