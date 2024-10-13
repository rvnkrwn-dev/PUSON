import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URI", "mysql+pymysql://root:@127.0.0.1/puson"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Secret keys
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "*YZTs96tyAGs685qw")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "UIAHs87uagsd")

    # JWT Cookie configuration
    app.config["JWT_ACCESS_COOKIE_NAME"] = "987AUgh8712gui"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "*&As6yuaiGS"

    JWTManager(app)

    with app.app_context():
        db.create_all()

    # Import and register Blueprint
    from .routes import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
