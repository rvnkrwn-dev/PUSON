from flask import Blueprint, make_response, request, jsonify
import logging
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from .models import User, RefreshToken, Log
from . import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .email_helper import send_email
import secrets


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
    new_user = User(
        full_name=full_name, email=email, password=hashed_password, role=role
    )

    db.session.add(new_user)
    try:
        db.session.commit()
        subject = "Registration Successful"
        body = "Your registration was successful, please wait for admin approval."
        send_email(subject, body, email)
        logging.info(f"Registered user: {new_user.email}")
        return (
            jsonify(
                {
                    "message": "Registration successful, notification email has been sent."
                }
            ),
            201,
        )
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

        new_refresh_token = RefreshToken(
            user_id=user.id, token=refresh_token, expires_at=expires_at
        )
        db.session.add(new_refresh_token)

        log_entry = Log(
            user_id=user.id,
            action="User Logged In",
            description="User successfully logged in and tokens were generated.",
        )
        db.session.add(log_entry)

        try:
            db.session.commit()
            logging.info(f"User logged in: {user.email}")

            # Create a response object
            response = make_response(
                jsonify(
                    {
                        "data": {
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                            "user": {"id": user.id, "email": user.email},
                        },
                        "message": "Successfully Login",
                        "statusCode": 200,
                    }
                )
            )

            response.set_cookie(
                "access_token", access_token, httponly=True, samesite="Lax"
            )
            response.set_cookie(
                "refresh_token", refresh_token, httponly=True, samesite="Lax"
            )

            return response, 200

        except Exception as e:
            db.session.rollback()
            logging.error(f"Failed to log in or save tokens: {e}")
            return jsonify({"message": "Failed to log in or save tokens"}), 500
    else:
        logging.warning(f"Failed login attempt for email: {email}")
        return jsonify({"message": "Invalid email or password"}), 401


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()

    logging.info(f"Refresh request from user ID: {identity}")

    token_entry = RefreshToken.query.filter_by(user_id=identity).first()

    if not token_entry:
        logging.warning(f"Invalid refresh token for user ID: {identity}")
        return jsonify({"message": "Invalid refresh token", "statusCode": 401}), 401

    if token_entry.expires_at < datetime.utcnow():
        logging.warning(f"Refresh token expired for user ID: {identity}")
        return jsonify({"message": "Refresh token expired", "statusCode": 401}), 401

    logging.info(f"Refresh token valid for user ID: {identity}")

    new_access_token = create_access_token(identity=identity, fresh=False)

    response = make_response(
        jsonify(
            {
                "data": {"access_token": new_access_token},
                "message": "Successfully refreshed access token",
                "statusCode": 200,
            }
        )
    )

    return response, 200


def is_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"message": "Token missing", "statusCode": 401}), 401

            token = token.split(" ")[1]

            jwt_data = get_jwt()
            print(f"Token Payload: {jwt_data}")

            exp = jwt_data.get("exp")
            print(f"Token Expiry: {exp}")

            if datetime.utcfromtimestamp(exp) < datetime.utcnow():
                return jsonify({"message": "Token expired", "statusCode": 401}), 401

            user_identity = get_jwt_identity()
            print(f"User ID: {user_identity}")

            return f(*args, **kwargs)

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"message": "Unauthorized", "statusCode": 401}), 401

    return decorated_function


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    try:
        jwt_data = get_jwt()
        user_id = jwt_data.get("sub")

        token_entry = RefreshToken.query.filter_by(user_id=user_id).first()

        if token_entry is None:
            return (
                jsonify(
                    {"message": "Token is invalid (logged out)", "statusCode": 401}
                ),
                401,
            )

        return jsonify({"message": f"Access granted for user ID {user_id}"}), 200

    except Exception as e:
        logging.error(f"Error accessing protected endpoint: {e}")
        return jsonify({"message": "Token invalid or expired", "statusCode": 401}), 401


@auth_bp.route("/user", methods=["GET"])
@jwt_required()
def user():
    identity = get_jwt_identity()

    logging.info(f"Refresh request from user ID: {identity}")

    token_entry = RefreshToken.query.filter_by(user_id=identity).first()

    if not token_entry:
        logging.warning(f"Invalid refresh token for user ID: {identity}")
        return jsonify({"message": "Invalid refresh token", "statusCode": 401}), 401

    if token_entry.expires_at < datetime.utcnow():
        logging.warning(f"Refresh token expired for user ID: {identity}")
        return jsonify({"message": "Refresh token expired", "statusCode": 401}), 401

    logging.info(f"Refresh token valid for user ID: {identity}")

    new_access_token = create_access_token(identity=identity, fresh=False)

    response = make_response(
        jsonify(
            {
                "data": {"access_token": new_access_token},
                "message": "Successfully refreshed access token",
                "statusCode": 200,
            }
        )
    )

    return response, 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        user_id = get_jwt_identity()

        token_entry = RefreshToken.query.filter_by(user_id=user_id).first()

        if token_entry:
            db.session.delete(token_entry)
            db.session.commit()
            logging.info(f"Refresh token for user ID {user_id} has been invalidated.")
        else:
            logging.warning(f"No refresh token found for user ID {user_id}")

        response = make_response(
            jsonify({"message": "Logout successful", "statusCode": 200})
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response, 200
    except Exception as e:
        logging.error(f"Error during logout: {e}")
        return jsonify({"message": "Logout failed", "statusCode": 500}), 500


def generate_and_send_token(email):
    token = secrets.token_urlsafe()

    user = User.query.filter_by(email=email).first()
    if user:
        user.reset_token = token
        user.reset_token_expiry = datetime.utcnow() + timedelta(hours=24)
        db.session.commit()

        return token
    return None


@auth_bp.route("/forget-password", methods=["POST"])
def forget_password():
    email = request.json.get("email")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Email not registered"}), 404

    token = generate_and_send_token(email)
    if not token:
        return jsonify({"message": "Failed to generate token"}), 500

    subject = "Password Reset"
    body = f"Your password reset link: {request.url_root}/auth/reset-password/{token}"

    try:
        send_email(subject, body, email)
    except Exception as e:
        return jsonify({"message": "Email send failed", "error": str(e)}), 500

    return jsonify({"message": "Password reset email sent"}), 200


@auth_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    data = request.json
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    user = User.query.filter_by(reset_token=token).first()
    if not user:
        return jsonify({"message": "Invalid token"}), 404

    token_expiry = user.reset_token_expiry
    if datetime.utcnow() > token_expiry:
        return jsonify({"message": "Expired token"}), 400

    if new_password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400

    hashed_password = generate_password_hash(
        new_password, method="scrypt", salt_length=10
    )

    user.password = hashed_password
    db.session.commit()

    return jsonify({"message": "Password has been reset successfully"}), 200
