from models.user_model import User
from models.transaction_model import Transaction
from database.db import db

def get_balance(name):
    user = User.query.filter_by(name=name).first()
    if not user:
        return {"msg": "User not found"}
    return {"balance": user.balance}


def deposit_money(name, amount):
    user = User.query.filter_by(name=name).first()

    user.balance += amount

    txn = Transaction(
        user_id=user.id,
        amount=amount,
        type="deposit",
        description="Money added"
    )

    db.session.add(txn)
    db.session.commit()

    return {"msg": "Deposit successful", "balance": user.balance}


def withdraw_money(name, amount):
    user = User.query.filter_by(name=name).first()

    if user.balance - amount < 1000:
        return {"msg": "Minimum balance should be ₹1000"}

    user.balance -= amount

    txn = Transaction(
        user_id=user.id,
        amount=amount,
        type="withdraw",
        description="Money withdrawn"
    )

    db.session.add(txn)
    db.session.commit()

    return {"msg": "Withdraw successful", "balance": user.balance}


def get_transactions(name):
    user = User.query.filter_by(name=name).first()

    txns = Transaction.query.filter_by(user_id=user.id).all()

    result = []
    for t in txns:
        result.append({
            "amount": t.amount,
            "type": t.type,
            "desc": t.description
        })

    return result