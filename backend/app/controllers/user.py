from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt, create_access_token
from ..middlewares.is_login import is_login
from ..middlewares.has_access import has_access
from ..models.user import User
from ..services.blacklisted_token import blacklisted_tokens
from .. import db

user_bp = Blueprint("user", __name__)


@user_bp.route("/user", methods=["GET"])
@jwt_required()
@is_login
def get_user():
    jwt_data = get_jwt()
    user_id = jwt_data.get("sub")
    jti = jwt_data.get("jti")

    if jti in blacklisted_tokens:
        return jsonify(
            {"message": "Token is invalid (logged out)", "statusCode": 401}
        ), 401

    user = User.query.get(user_id)
    if user:
        new_access_token = create_access_token(identity=user_id)
        response = make_response(
            jsonify(
                {
                    "data": {"access_token": new_access_token},
                    "message": "Successfully refreshed access token",
                    "statusCode": 200,
                }
            )
        )
        return response

    return jsonify({"message": "User not found", "statusCode": 404}), 404


@user_bp.route("/user", methods=["POST"])
@jwt_required()
@is_login
def create_user():
    data = request.json
    try:
        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "user")

        if not all([full_name, email, password]):
            return jsonify(
                {"message": "Missing required fields", "statusCode": 400}
            ), 400

        new_user = User(full_name=full_name, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully", "statusCode": 201}), 201
    except Exception as e:
        return jsonify({"message": str(e), "statusCode": 500}), 500


@user_bp.route("/user/<int:id>", methods=["PUT"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu"])
def update_user(id):
    data = request.json
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found", "statusCode": 404}), 404

        for key, value in data.items():
            if key == "password":
                user.set_password(value)
            else:
                setattr(user, key, value)

        db.session.commit()
        return jsonify({"message": "User updated successfully", "statusCode": 200}), 200
    except Exception as e:
        return jsonify({"message": str(e), "statusCode": 500}), 500


@user_bp.route("/user/<int:id>", methods=["DELETE"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu"])
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found", "statusCode": 404}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully", "statusCode": 200}), 200
    except Exception as e:
        return jsonify({"message": str(e), "statusCode": 500}), 500
