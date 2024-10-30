from flask import Blueprint, make_response, request, jsonify
import logging
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    decode_token
)
from ..models import User, RefreshToken, Log
from .. import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from ..services.email_helper import send_email
from ..middlewares.is_login import is_login
import secrets
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect

load_dotenv()

csrf = CSRFProtect()
auth_bp = Blueprint("auth", __name__)

logging.basicConfig(level=logging.DEBUG)

@auth_bp.route("/register", methods=["POST"])
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
    new_user = User(full_name=full_name, email=email, password=hashed_password, role=role)

    db.session.add(new_user)
    try:
        db.session.commit()
        subject = "Registration Successful"
        body = "Your registration was successful, please wait for admin approval."
        send_email(subject, body, email)
        logging.info(f"Registered user: {new_user.email}")
        return jsonify({"message": "Registration successful, notification email has been sent."}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Failed to register user: {e}")
        return jsonify({"message": "Failed to register user"}), 500

@auth_bp.route("/login", methods=["POST"])
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

        new_refresh_token = RefreshToken(user_id=user.id, token=refresh_token, expires_at=expires_at)
        db.session.add(new_refresh_token)

        log_entry = Log(user_id=user.id, action="User Logged In", description="User successfully logged in and tokens were generated.")
        db.session.add(log_entry)

        try:
            db.session.commit()
            logging.info(f"User logged in: {user.email}")

            response = make_response(jsonify({
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"id": user.id, "email": user.email},
                },
                "message": "Successfully Login",
                "statusCode": 200,
            }))
            response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite="Strict")
            return response, 200

        except Exception as e:
            db.session.rollback()
            logging.error(f"Failed to log in or save tokens: {e}")
            return jsonify({"message": "Failed to log in or save tokens"}), 500
    else:
        logging.warning(f"Failed login attempt for email: {email}")
        return jsonify({"message": "Invalid email or password"}), 401

@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        logging.warning("No refresh token found in the request cookies.")
        return jsonify({"message": "Missing refresh token"}), 400

    try:
        decoded_token = decode_token(refresh_token)
        logging.info(f"Decoded token: {decoded_token}")

        user_id = decoded_token.get("sub")

        if not user_id:
            logging.error("Invalid refresh token: Missing user ID (sub).")
            return jsonify({"message": "Invalid refresh token"}), 401

        new_access_token = create_access_token(identity=user_id)

        return jsonify({
            "data": {"access_token": new_access_token},
            "message": "Token refreshed successfully",
            "statusCode": 200,
        }), 200

    except Exception as e:
        logging.error(f"Failed to refresh token: {e}")
        return jsonify({"message": "Invalid refresh token"}), 401

@auth_bp.route("/user", methods=["GET"])
@jwt_required()
@is_login
def user():
    user_id = get_jwt_identity()
    return jsonify({"message": f"Access granted for user ID {user_id}"}), 200

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        user_id = get_jwt_identity()

        token_entry = RefreshToken(user_id=user_id, token=jti, expires_at=datetime.utcnow() + timedelta(hours=1)) 
        db.session.add(token_entry)
        db.session.commit()

        logging.info(f"Invalidating access token for user ID: {user_id}")

        response = jsonify({"message": "Successfully logged out"})
        response.delete_cookie("refresh_token")
        return response, 200
    except Exception as e:
        logging.error(f"Failed to log out: {e}")
        return jsonify({"message": "Failed to log out"}), 500

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"message": "Missing email"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Email not found"}), 404

    reset_token = secrets.token_urlsafe(16)
    user.reset_token = reset_token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)

    db.session.commit()

    reset_link = f"http://localhost:5000/reset-password/{reset_token}"
    subject = "Reset Password Request"
    body = f"Click the link to reset your password: {reset_link}"

    send_email(subject, body, email)

    logging.info(f"Reset password link sent to: {email}")
    return jsonify({"message": "Reset password link sent"}), 200

@auth_bp.route("/reset-password/<token>", methods=["POST"])
def update_password(token):
    data = request.get_json()
    new_password = data.get("new_password")

    if not new_password:
        return jsonify({"message": "Missing new password"}), 400

    user = User.query.filter_by(reset_token=token).first()
    if not user or user.reset_token_expiry < datetime.utcnow():
        return jsonify({"message": "Invalid or expired token"}), 400

    user.password = generate_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expiry = None

    db.session.commit()
    logging.info(f"Password updated for user ID: {user.id}")

    return jsonify({"message": "Password updated successfully"}), 200
