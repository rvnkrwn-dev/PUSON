import os
from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('DATABASE_USER')}:"
        f"{os.getenv('DATABASE_PASSWORD')}@"
        f"{os.getenv('DATABASE_HOST')}/"
        f"{os.getenv('DATABASE_NAME')}"
    )
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "UIAHs87uagsd")

    app.config["JWT_ACCESS_COOKIE_NAME"] = "987AUgh8712gui"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "*&As6yuaiGS"

    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]


    jwt = JWTManager(app)
    
    with app.app_context():
        db.create_all()
        from .controllers import init_auth_blueprints

        init_auth_blueprints(app)

    return app
