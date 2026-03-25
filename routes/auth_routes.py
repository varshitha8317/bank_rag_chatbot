from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user

auth_bp = Blueprint("auth", __name__)


# 🟢 REGISTER ROUTE
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    name = data.get("name")
    password = data.get("password")
    account_type = data.get("account_type", "savings")

    if not name or not password:
        return jsonify({"msg": "Name and password required"}), 400

    result = register_user(name, password, account_type)
    return jsonify(result)


# 🔐 LOGIN ROUTE
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    name = data.get("name")
    password = data.get("password")

    if not name or not password:
        return jsonify({"msg": "Name and password required"}), 400

    result = login_user(name, password)
    return jsonify(result)