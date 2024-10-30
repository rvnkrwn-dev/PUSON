from flask import Blueprint, jsonify, request, make_response
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from ..models.user import User
from ..models.refresh_token import RefreshToken
from ..models.log import Log
import logging
from datetime import datetime, timedelta
from .. import db

login_bp = Blueprint("login", __name__)
logging.basicConfig(level=logging.DEBUG)


@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        expires_at = datetime.utcnow() + timedelta(days=1)
        new_refresh_token = RefreshToken(
            user_id=user.id, token=refresh_token, expires_at=expires_at
        )
        db.session.add(new_refresh_token)

        log_entry = Log(
            user_id=user.id, action="User Logged In", description="Tokens generated."
        )
        db.session.add(log_entry)

        try:
            db.session.commit()
            response = make_response(
                jsonify(
                    {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": {"id": user.id, "email": user.email},
                    }
                )
            )
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                secure=True,
                samesite="Strict",
            )
            return response, 200
        except Exception as e:
            db.session.rollback()
            logging.error(f"Failed to log in or save tokens: {e}")
            return jsonify({"message": "Failed to log in"}), 500
    else:
        return jsonify({"message": "Invalid email or password"}), 401
