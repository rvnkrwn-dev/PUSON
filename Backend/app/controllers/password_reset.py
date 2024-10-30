from flask import Blueprint, jsonify, request
from ..models.user import User
from ..services.email_helper import send_email
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import secrets


password_reset_bp = Blueprint("password_reset", __name__)


@password_reset_bp.route("/forget-password", methods=["POST"])
def forget_password():
    from app import db
    email = request.json.get("email")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Email not registered"}), 404

    token = secrets.token_urlsafe()
    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=24)
    db.session.commit()
    send_email(
        "Password Reset",
        f"Reset link: {request.url_root}/auth/reset-password/{token}",
        email,
    )
    return jsonify({"message": "Password reset email sent"}), 200


@password_reset_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    from app import db
    data = request.json
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")
    user = User.query.filter_by(reset_token=token).first()
    if not user or datetime.utcnow() > user.reset_token_expiry:
        return jsonify({"message": "Invalid or expired token"}), 404

    if new_password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400

    user.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({"message": "Password has been reset successfully"}), 200
