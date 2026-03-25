from models.user_model import User
from database.db import db
from flask_jwt_extended import create_access_token


# 🔐 REGISTER USER
def register_user(name, password, account_type):
    # check if user already exists
    existing_user = User.query.filter_by(name=name).first()

    if existing_user:
        return {"msg": "User already exists"}

    # create new user
    new_user = User(
        name=name,
        password=password,
        balance=0,
        account_type=account_type
    )

    db.session.add(new_user)
    db.session.commit()

    return {"msg": "User registered successfully"}


# 🔐 LOGIN USER
def login_user(name, password):
    user = User.query.filter_by(name=name).first()

    if not user:
        return {"msg": "User not found"}

    if user.password != password:
        return {"msg": "Incorrect password"}

    # create JWT token
    token = create_access_token(identity=user.name)

    return {
        "msg": "Login successful",
        "token": token
    }