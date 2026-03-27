from models.user_model import User
from models.transaction_model import Transaction
from database.db import db
from services.sns_service import send_alert
from services.sqs_service import send_to_queue

def get_balance(name):
    user = User.query.filter_by(name=name).first()
    if not user:
        return {"msg": "User not found"}
    return {"balance": user.balance}


def deposit_money(name, amount):
    user = User.query.filter_by(name=name).first()

    if not user:
        return {"msg": "User not found"}

    user.balance += amount

    txn = Transaction(
        user_id=user.id,
        amount=amount,
        type="deposit",
        description="Money added"
    )

    db.session.add(txn)

    # 📩 SQS LOG
    send_to_queue(f"{name} deposited ₹{amount}")

    db.session.commit()

    return {"msg": "Deposit successful", "balance": user.balance}

def withdraw_money(name, amount):
    user = User.query.filter_by(name=name).first()

    if not user:
        return {"msg": "User not found"}

    # ✅ Rule check
    if user.balance - amount < 1000:
        return {"msg": "Minimum balance should be ₹1000"}

    # ✅ Deduct balance
    user.balance -= amount

    # ✅ Create transaction
    txn = Transaction(
        user_id=user.id,
        amount=amount,
        type="withdraw",
        description="Money withdrawn"
    )

    db.session.add(txn)

    # 🔔 SNS ALERT (ONLY FOR HIGH AMOUNT)
    if amount > 10000:
        send_alert(f"⚠ High withdrawal of ₹{amount} by {name}")

    # 📩 SQS MESSAGE (FOR EVERY TRANSACTION)
    send_to_queue(f"{name} withdrew ₹{amount}")

    # ✅ Save to DB
    db.session.commit()

    return {"msg": "Withdraw successful", "balance": user.balance}



def get_transactions(name):
    user = User.query.filter_by(name=name).first()

    if not user:
        return {"msg": "User not found"}   # ✅ fix

    txns = Transaction.query.filter_by(user_id=user.id).all()

    result = []
    for t in txns:
        result.append({
            "amount": t.amount,
            "type": t.type,
            "desc": t.description
        })

    return result