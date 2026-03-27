from flask import Blueprint, request, jsonify
from services.rag_service import get_answer
from services.db_service import get_balance, get_transactions
from services.llm_service import ask_llm

chat_bp = Blueprint("chat", __name__)

BANK_KEYWORDS = [
    "bank", "account", "balance", "deposit",
    "withdraw", "loan", "transaction", "credit", "debit"
]


@chat_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        query = data.get("query", "").lower()
        user = data.get("user", "Varsha")   # ✅ default user (fix)

        if not query:
            return jsonify({"error": "Query is required"}), 400

        # -----------------------------
        # 🟢 DB LOGIC (IMPROVED 🔥)
        # -----------------------------
        if any(word in query for word in ["balance", "my balance", "account balance"]):
            return jsonify(get_balance(user))

        elif any(word in query for word in ["transaction", "transactions", "history"]):
            return jsonify(get_transactions(user))

        # -----------------------------
        # 🟢 RAG (FAQ)
        # -----------------------------
        answer = get_answer(query)

        if answer and any(word in query for word in BANK_KEYWORDS):
            return jsonify({
                "answer": answer,
                "source": "faq"
            })

        # -----------------------------
        # 🔥 GEMINI
        # -----------------------------
        ai_answer = ask_llm(query)

        return jsonify({
            "answer": ai_answer,
            "source": "gemini"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500