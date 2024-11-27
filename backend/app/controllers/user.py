from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt
from ..middlewares.is_login import is_login
from ..models.user import User
from ..services.blacklisted_token import blacklisted_tokens
from .. import db

user_bp = Blueprint("user", __name__)


@user_bp.route("/user", methods=["GET"])
@jwt_required()
@is_login
def get_user():
    # Mengambil data JWT dari permintaan
    jwt_data = get_jwt()
    user_id = jwt_data.get("sub")  # Mendapatkan ID pengguna dari token
    jti = jwt_data.get("jti")  # Mendapatkan JTI (JWT ID) dari token

    # Memeriksa apakah token ada dalam daftar blacklist
    if jti in blacklisted_tokens:
        return jsonify(
            {"message": "Token tidak valid (sudah logout)", "statusCode": 401}
        ), 401

    # Mencari pengguna berdasarkan ID
    user = User.query.get(user_id)
    if user:
        # Membuat respons dengan detail pengguna
        response = make_response(
            jsonify(
                {
                    "data": {
                        "id": user.id,
                        "full_name": user.full_name,
                        "email": user.email,
                        "role": user.role,
                    },
                    "statusCode": 200,
                }
            )
        )
        response.status_code = 200
        return response

    # Mengembalikan respons jika pengguna tidak ditemukan
    return jsonify({"message": "Pengguna tidak ditemukan", "statusCode": 404}), 404
