from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from ..models.user import User
from ..services.email_helper import send_email
import logging
from .. import db

register_bp = Blueprint("register", __name__)
logging.basicConfig(level=logging.DEBUG)


@register_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not all([full_name, email, password, role]):
        return jsonify({"message": "Missing data"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(
        full_name=full_name, email=email, password=hashed_password, role=role
    )

    db.session.add(new_user)
    try:
        db.session.commit()
        send_email("Registration Successful", "Please wait for admin approval.", email)
        logging.info(f"Registered user: {new_user.email}")
        return jsonify({"message": "Registration successful."}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Failed to register user: {e}")
        return jsonify({"message": "Failed to register user"}), 500