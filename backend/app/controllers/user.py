from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt, create_access_token
from ..middlewares.is_login import is_login
from ..models import RefreshToken
from ..models.user import User

user_bp = Blueprint("user", __name__)

@user_bp.route("/user", methods=["GET"])
@jwt_required()
@is_login
def user():
    jwt_data = get_jwt()
    user_id = jwt_data.get("sub")
    jti = jwt_data.get("jti")

    token_entry = RefreshToken.query.filter_by(user_id=user_id, token=jti).first()

    if token_entry:
        return (
            jsonify(
                {"message": "Token is invalid (logged out)", "statusCode": 401}
            ),
            401,
        )

    else:
        jsonify({"message": f"Access granted for user ID {user_id}"}), 200

    new_access_token = create_access_token(identity=user_id, fresh=False)

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
