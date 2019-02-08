import db
from decimal import Decimal

def get_user(user_id):
    with db.connect() as cursor:
        cursor.execute("SELECT username, balance from users where id = %s", (user_id,))
        return cursor.fetchone()
    
    return None

def get_user_id(username):
    with db.connect() as cursor:
        cursor.execute("SELECT id from users where username = %s", (username.lower(),))
        result = cursor.fetchone()

        return result["id"] if result else None
    
    return None

# in a real system these ops need to be atomic. this is a fake payment app so nah lol
def user_has_enough_funds(uid, amt):
    user = get_user(uid)
    balance = user["balance"]
    
    return balance - Decimal(amt) >= Decimal(0)