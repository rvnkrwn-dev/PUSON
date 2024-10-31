from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt, create_access_token
from ..middlewares.is_login import is_login
from ..models.user import User
from ..services.blacklisted_token import blacklisted_tokens

user_bp = Blueprint("user", __name__)


@user_bp.route("/user", methods=["GET"])
@jwt_required()
@is_login
def user():
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
