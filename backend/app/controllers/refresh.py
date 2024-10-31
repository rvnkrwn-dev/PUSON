from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
import logging
from ..models.refresh_token import validate_token
from .. import db

refresh_bp = Blueprint("refresh", __name__)
logging.basicConfig(level=logging.DEBUG)


@refresh_bp.route("/refresh", methods=["POST"])
def refresh():
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return jsonify({"message": "Missing refresh token"}), 400

    valid_token_entry = validate_token(db.session, refresh_token)
    if not valid_token_entry:
        return jsonify({"message": "Invalid refresh token"}), 401

    try:
        user_id = valid_token_entry.user_id
        new_access_token = create_access_token(identity=user_id)

        return jsonify({"access_token": new_access_token}), 200
    except Exception as e:
        logging.error(f"Failed to refresh token: {e}")
        return jsonify({"message": "Could not refresh token"}), 500
