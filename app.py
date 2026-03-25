from flask import Flask
from database.db import db
from config import DB_URI, JWT_SECRET
from flask_jwt_extended import JWTManager

from routes.auth_routes import auth_bp
from routes.bank_routes import bank_bp
from routes.chat_routes import chat_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['JWT_SECRET_KEY'] = JWT_SECRET

db.init_app(app)
jwt = JWTManager(app)

# Register routes
app.register_blueprint(auth_bp)
app.register_blueprint(bank_bp)
app.register_blueprint(chat_bp)

# Create tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)