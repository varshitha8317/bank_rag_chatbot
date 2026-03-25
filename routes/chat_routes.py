from flask import Blueprint, request, jsonify
from services.rag_service import get_answer
from services.db_service import get_balance, get_transactions

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    query = request.json["query"].lower()

    # 🔥 DATABASE QUESTIONS
    if "balance" in query:
        return jsonify(get_balance("Varsha"))

    elif "transaction" in query:
        return jsonify(get_transactions("Varsha"))

    # 🔥 DEFAULT → RAG
    answer = get_answer(query)
    return jsonify({"answer": answer})