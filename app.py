from flask import Flask, render_template
from database.db import db
from config import DB_URI, JWT_SECRET
from flask_jwt_extended import JWTManager

# Routes
from routes.auth_routes import auth_bp
from routes.bank_routes import bank_bp
from routes.chat_routes import chat_bp

app = Flask(__name__)

# -----------------------------
# CONFIG
# -----------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['JWT_SECRET_KEY'] = JWT_SECRET
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -----------------------------
# INIT
# -----------------------------
db.init_app(app)
jwt = JWTManager(app)

# -----------------------------
# FRONTEND ROUTE
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -----------------------------
# REGISTER ROUTES
# -----------------------------
app.register_blueprint(auth_bp)
app.register_blueprint(bank_bp)
app.register_blueprint(chat_bp)

# -----------------------------
# CREATE TABLES
# -----------------------------
with app.app_context():
    db.create_all()

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)