from flask import Blueprint, make_response, request, jsonify
import logging
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    verify_jwt_in_request,
    jwt_required,
    get_jwt_identity,
)
from .models import User
from . import db
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from werkzeug.security import generate_password_hash
from functools import wraps
from .email_helper import send_email
import secrets


auth_bp = Blueprint("auth", __name__)

logging.basicConfig(level=logging.DEBUG)


@auth_bp.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    name = request.json.get("name")
    address = request.json.get("address")
    role_id = request.json.get("role_id")
    posyandu_id = request.json.get("posyandu_id")

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409

    hashed_password = generate_password_hash(password, method='scrypt', salt_length=10)

    new_user = User(
        username=username,
        password=hashed_password,
        email=email,
        name=name,
        address=address,
        role_id=role_id,
        posyandu_id=posyandu_id,
    )

    db.session.add(new_user)
    db.session.commit()

    subject = "Registrasi Berhasil"
    body = "Registrasi berhasil, tunggu di setujui oleh admin."
    send_email(subject, body, email)

    print(f"Registered user: {new_user.username}")

    return jsonify({"message": "Registrasi berhasil, email notifikasi telah dikirim."})


@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # Generate tokens
        access_token = create_access_token(
            identity=username, expires_delta=timedelta(minutes=15)
        )
        refresh_token = create_refresh_token(
            identity=username, expires_delta=timedelta(days=1)
        )

        response = jsonify(
            {
                "statusCode": 200,
                "message": "Successfully Login",
                "data": {
                    "access_token": access_token,
                    "user": {"id": user.id, "username": user.username},
                },
            }
        )
        response.set_cookie(
            "refresh_token_cookie", refresh_token, httponly=True, secure=True
        )
        return response, 200

    if user:
        print(f"Stored hash: {user.password}")

    return jsonify({"statusCode": 403, "message": "Invalid credentials"}), 403


@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    refresh_token = request.cookies.get("refresh_token_cookie")

    if not refresh_token:
        return jsonify({"message": "Refresh token not found"}), 401

    try:
        decoded_token = jwt.decode(refresh_token, options={"verify_signature": False})
        identity = decoded_token["sub"]
        user = User.query.filter_by(username=identity).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        new_access_token = create_access_token(
            identity=identity, expires_delta=timedelta(minutes=15)
        )
        return (
            jsonify(
                {
                    "access_token": new_access_token,
                    "user": {"id": user.id, "username": user.username},
                }
            ),
            200,
        )
    except ExpiredSignatureError:
        return jsonify({"message": "Refresh token has expired"}), 401
    except InvalidTokenError:
        return jsonify({"message": "Invalid refresh token"}), 401
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


def isLogin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            print(f"Request headers: {request.headers}")
            
            verify_jwt_in_request()
            
            current_user = get_jwt_identity()
            print(f"Current user: {current_user}")
        except Exception as e:
            print(
                f"JWT verification failed: {e}"
            )
            return jsonify({"message": "Unauthorized", "error": str(e)}), 401
        return f(*args, **kwargs)

    return decorated_function


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"This is a protected route, {current_user}"}), 200


@auth_bp.route("/user", methods=["GET"])
@isLogin
def user():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({"user": {"id": user.id, "username": user.username}}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"message": "You have been logged out"}))

    response.delete_cookie("refresh_token_cookie")

    return response


def generate_and_send_token(email):
    token = secrets.token_urlsafe()

    user = User.query.filter_by(email=email).first()
    if user:
        user.reset_token = token
        user.reset_token_expiry = datetime.utcnow() + timedelta(
            hours=24
        )
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

    hashed_password = generate_password_hash(new_password, method='scrypt', salt_length=10)

    user.password = hashed_password
    db.session.commit()

    return jsonify({"message": "Password has been reset successfully"}), 200
