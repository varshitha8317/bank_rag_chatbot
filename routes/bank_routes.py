from flask import Blueprint, request, jsonify
from services.db_service import get_balance, deposit_money, withdraw_money, get_transactions
from flask_jwt_extended import jwt_required

bank_bp = Blueprint("bank", __name__)

@bank_bp.route("/balance", methods=["GET"])
@jwt_required()
def balance():
    name = request.args.get("name")
    return jsonify(get_balance(name))


@bank_bp.route("/deposit", methods=["POST"])
@jwt_required()
def deposit():
    data = request.json
    return jsonify(deposit_money(data["name"], data["amount"]))


@bank_bp.route("/withdraw", methods=["POST"])
@jwt_required()
def withdraw():
    data = request.json
    return jsonify(withdraw_money(data["name"], data["amount"]))


@bank_bp.route("/transactions", methods=["GET"])
@jwt_required()
def transactions():
    name = request.args.get("name")
    return jsonify(get_transactions(name))