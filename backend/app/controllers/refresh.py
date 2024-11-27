from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
import logging
from ..models.refresh_token import validate_token
from .. import db

refresh_bp = Blueprint("refresh", __name__)
logging.basicConfig(level=logging.DEBUG)


@refresh_bp.route("/refresh", methods=["POST"])
def refresh():
    # Mengambil refresh token dari cookie
    refresh_token = request.cookies.get("refresh_token")
    
    # Memeriksa apakah refresh token ada
    if not refresh_token:
        return jsonify({"message": "Token refresh tidak ditemukan"}), 400

    # Memvalidasi refresh token
    valid_token_entry = validate_token(db.session, refresh_token)
    
    # Memeriksa apakah token valid
    if not valid_token_entry:
        return jsonify({"message": "Token refresh tidak valid"}), 401

    try:
        user_id = valid_token_entry.user_id  # Mengambil ID pengguna dari token yang valid
        new_access_token = create_access_token(identity=str(user_id))  # Membuat token akses baru

        # Mengembalikan respons dengan token akses baru
        return jsonify({"access_token": new_access_token}), 200
    except Exception as e:
        logging.error(f"Gagal untuk memperbarui token: {e}")  # Mencatat kesalahan
        return jsonify({"message": "Gagal untuk memperbarui token"}), 500
