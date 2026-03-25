from database.db import db

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    type = db.Column(db.String(10))  # deposit / withdraw
    description = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=db.func.current_timestamp())