from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from ..models import RefreshToken
import logging
from .. import db

logout_bp = Blueprint("logout", __name__)
logging.basicConfig(level=logging.DEBUG)


@logout_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        user_id = get_jwt_identity()
        token_entry = RefreshToken(
            user_id=user_id,
            token=jti,
            expires_at=datetime.utcnow() + timedelta(hours=1),
        )
        db.session.add(token_entry)
        db.session.commit()
        response = jsonify({"message": "Logout successful"})
        response.delete_cookie("refresh_token")
        response.delete_cookie("access_token")
        return response, 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Logout error: {e}")
        return jsonify({"message": "Logout error"}), 500
