import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URI", "mysql+pymysql://root:@127.0.0.1/puson_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Secret keys
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "*YZTs96tyAGs685qw")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "UIAHs87uagsd")

    # JWT Cookie configuration
    app.config["JWT_ACCESS_COOKIE_NAME"] = "987AUgh8712gui"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "*&As6yuaiGS"


    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()

    # Import and register Blueprint
    from .routes import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    # # Configure Flask-Mail with SMTP server details
    # app.config["MAIL_SERVER"] = "smtp-relay.brevo.com"
    # app.config["MAIL_PORT"] = 587
    # app.config["MAIL_USE_TLS"] = True
    # app.config["MAIL_USERNAME"] = os.getenv(
    #     "7d5b94001@smtp-brevo.com"
    # )
    # app.config["MAIL_PASSWORD"] = os.getenv("m8xD1nUcgQBpqjkW")
    # mail = Mail(app)

    return app
