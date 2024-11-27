from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from ..models.log import add_log
from .. import db
from ..services.blacklisted_token import blacklisted_tokens
from datetime import datetime
from ..models.refresh_token import delete_refresh_token

logout_bp = Blueprint("logout", __name__)


@logout_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        # Mengambil JTI (JWT ID) dan ID pengguna dari token
        jti = get_jwt()["jti"]
        user_id = get_jwt_identity()

        # Menambahkan JTI ke daftar token yang diblacklist
        blacklisted_tokens.add(jti)

        # Menghapus refresh token yang terkait dengan pengguna
        delete_refresh_token(db.session, user_id)

        # Menambahkan log untuk aktivitas keluar
        add_log(db.session, user_id, "Pengguna keluar", "Pengguna telah berhasil keluar.")

        # Membuat respons JSON untuk keluar yang berhasil
        response = jsonify({"message": "Berhasil keluar"})

        # Menghapus cookie refresh token
        response.set_cookie(
            "refresh_token",
            "",
            expires=datetime.utcnow(),
            httponly=True,
            secure=True,
            samesite="None",
        )

        return response, 200

    except Exception:
        # Menggulung kembali sesi jika terjadi kesalahan
        db.session.rollback()
        return jsonify({"message": "Terjadi kesalahan saat keluar"}), 500
