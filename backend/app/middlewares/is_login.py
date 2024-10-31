from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity, get_jwt, verify_jwt_in_request
from ..models.user import User


def is_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()

            jwt_data = get_jwt()
            if current_app.debug:
                print(f"Token Payload: {jwt_data}")

            user_id = get_jwt_identity()

            user = User.query.get(user_id)
            if not user:
                return jsonify({"message": "Token is invalid"}), 401

            request.user = user
            return f(*args, **kwargs)

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"message": "Unauthorized", "statusCode": 401}), 401

    return decorated_function
