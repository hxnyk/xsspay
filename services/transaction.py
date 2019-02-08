import db
import time
from decimal import Decimal
from . import user

# This is not atomic so it has an obvious race condition that any bank or payment app would be sad to have
# sender = uid, receiver = username, amount = value, description = str, is_payment=True
def perform_transaction(sender, receiver, amount, description, is_payment=True):
    sender_id = sender
    receiver_id = user.get_user_id(receiver)

    actual_sender_id = sender_id
    actual_receiver_id = receiver_id

    if not is_payment:
        actual_sender_id = receiver_id
        actual_receiver_id = sender_id

    sender_user = user.get_user(actual_sender_id)
    receiver_user = user.get_user(actual_receiver_id)

    # sender have enough?
    if user.user_has_enough_funds(actual_sender_id, amount):
        # act
        sender_new = sender_user["balance"] - Decimal(amount)
        receiver_new = receiver_user["balance"] + Decimal(amount)

        with db.connect() as cursor:
            cursor.execute("UPDATE users SET balance=%s where id=%s", (sender_new, actual_sender_id))
            cursor.execute("UPDATE users SET balance=%s where id=%s", (receiver_new, actual_receiver_id))
            cursor.execute(
                "INSERT INTO transactions (sender, receiver, amt, description, timestamp) VALUES (%s, %s, %s, %s, %s)",
                (actual_sender_id,
                actual_receiver_id,
                Decimal(amount),
                description,
                int(time.time()))
            )
            return True
    else:
        return False


def get_transactions_for_user(uid):
    with db.connect() as cursor:
        cursor.execute("SELECT * from transactions where sender = %s or receiver = %s", (uid, uid))
        return cursor.fetchall()
    
    return None

def get_readable_transactions_for_user(uid):
    transactions = get_transactions_for_user(uid)

    results = []

    transactions.sort(key=lambda x: x["timestamp"], reverse=True)

    for transaction in transactions:
        # other party
        # how much
        # type
        # description

        sender_uid = transaction["sender"]
        receiver_uid = transaction["receiver"]
        amount = transaction["amt"]
        description = transaction["description"]
        
        other_uid = sender_uid if sender_uid != uid else receiver_uid
        payment_type = other_uid == receiver_uid # true = pay; false = request
        
        other_username = user.get_user(other_uid)["username"]

        results.append({
            "name": other_username,
            "amount": amount,
            "type": "pay" if payment_type else "request",
            "description": description
        })
    
    return results