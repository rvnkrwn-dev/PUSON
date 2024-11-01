from flask import Blueprint, jsonify, request
from ..models.user import User, updateUser
from ..services.email_helper import send_email
from datetime import datetime, timedelta
import secrets

forget_password_bp = Blueprint("password_reset", __name__)


@forget_password_bp.route("/forget-password", methods=["POST"])
def forget_password():
    email = request.json.get("email")
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "Email not registered"}), 404

    token = secrets.token_urlsafe()
    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=24)

    updateUser(
        user.id, {"reset_token": token, "reset_token_expiry": user.reset_token_expiry}
    )

    send_email(
        "Password Reset",
        f"Reset link: {request.url_root}/auth/reset-password/{token}",
        email,
    )
    return jsonify({"message": "Password reset email sent"}), 200
