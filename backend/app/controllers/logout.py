from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from ..models.log import add_log
from .. import db
from ..services.blacklisted_token import blacklisted_tokens

logout_bp = Blueprint("logout", __name__)


@logout_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        user_id = get_jwt_identity()

        blacklisted_tokens.add(jti)

        add_log(db.session, user_id, "User Logout", "User has logged out successfully.")

        response = jsonify({"message": "Logout successful"})
        response.delete_cookie("refresh_token")
        response.delete_cookie("access_token")

        return response, 200

    except Exception:
        db.session.rollback()
        return jsonify({"message": "Logout error"}), 500
