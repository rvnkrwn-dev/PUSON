from flask import Blueprint, jsonify, request
from flask_jwt_extended import decode_token, create_access_token
import logging


refresh_bp = Blueprint("refresh", __name__)
logging.basicConfig(level=logging.DEBUG)


@refresh_bp.route("/refresh", methods=["POST"])
def refresh():
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return jsonify({"message": "Missing refresh token"}), 400

    try:
        decoded_token = decode_token(refresh_token)
        user_id = decoded_token.get("sub")
        if not user_id:
            return jsonify({"message": "Invalid refresh token"}), 401
        new_access_token = create_access_token(identity=user_id)
        return jsonify({"access_token": new_access_token}), 200
    except Exception as e:
        logging.error(f"Failed to refresh token: {e}")
        return jsonify({"message": "Invalid refresh token"}), 401
