from flask import Blueprint, jsonify, request
from ..models.user import User, updateUser
from datetime import datetime

reset_password_bp = Blueprint("reset_password", __name__)


@reset_password_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    data = request.json
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    user = User.query.filter_by(reset_token=token).first()

    if not user or datetime.utcnow() > user.reset_token_expiry:
        return jsonify({"message": "Invalid or expired token"}), 404

    if new_password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400

    updateUser(
        user.id,
        {
            "password": new_password,
            "reset_token": None,
            "reset_token_expiry": None,
        },
    )

    return jsonify({"message": "Password has been reset successfully"}), 200
