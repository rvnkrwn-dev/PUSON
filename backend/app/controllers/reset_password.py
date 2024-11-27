from flask import Blueprint, jsonify, request
from ..models.user import User, updateUser
from datetime import datetime

reset_password_bp = Blueprint("reset_password", __name__)


@reset_password_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    # Mengambil data JSON dari permintaan
    data = request.json
    new_password = data.get("new_password")  # Mendapatkan kata sandi baru
    confirm_password = data.get("confirm_password")  # Mendapatkan konfirmasi kata sandi

    # Mencari pengguna berdasarkan token reset
    user = User.query.filter_by(reset_token=token).first()

    # Memeriksa apakah pengguna ditemukan dan apakah token sudah kedaluwarsa
    if not user or datetime.utcnow() > user.reset_token_expiry:
        return jsonify({"message": "Token tidak valid atau sudah kedaluwarsa"}), 404

    # Memeriksa apakah kata sandi baru dan konfirmasi kata sandi cocok
    if new_password != confirm_password:
        return jsonify({"message": "Kata sandi tidak cocok"}), 400

    # Memperbarui kata sandi pengguna dan menghapus token reset
    updateUser(
        user.id,
        {
            "password": new_password,
            "reset_token": None,
            "reset_token_expiry": None,
        },
    )

    # Mengembalikan respons sukses setelah reset kata sandi
    return jsonify({"message": "Kata sandi telah berhasil direset"}), 200
