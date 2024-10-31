from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from ..models.user import authenticate
from ..models.refresh_token import generate_token
from ..models.log import add_log
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

    user = authenticate(email, password)
    if user:
        access_token = create_access_token(
            identity=user["id"], expires_delta=timedelta(minutes=15)
        )

        refresh_token = create_refresh_token(identity=user["id"])

        expires_at = datetime.utcnow() + timedelta(days=7)

        new_refresh_token = generate_token(
            db.session, user["id"], refresh_token, expires_at
        )

        add_log(db.session, user["id"], "User Logged In", "Tokens generated.")

        try:
            db.session.commit()
            response = make_response(
                jsonify(
                    {
                        "access_token": access_token,
                        "refresh_token": new_refresh_token.token,
                        "expires_at": expires_at.isoformat(),
                        "user": {"id": user["id"], "email": user["email"]},
                    }
                )
            )
            logging.debug(f"Generated refresh token: {new_refresh_token.token}")
            response.set_cookie(
                "refresh_token",
                new_refresh_token.token,
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
