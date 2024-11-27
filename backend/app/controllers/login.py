from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from ..models.user import authenticate
from ..models.refresh_token import generate_token
from ..models.log import add_log
from datetime import datetime, timedelta
from .. import db

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["POST"])
def login():
    # Mengambil data JSON dari permintaan
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Memeriksa apakah email dan password disediakan
    if not email or not password:
        return jsonify({"message": "Email atau kata sandi tidak boleh kosong"}), 400

    # Mengautentikasi pengguna
    user = authenticate(email, password)
    if user:
        user_id = user["id"]
        full_name = user.get("full_name")
        role = user.get("role")
        
        # Membuat token akses dan refresh baru
        access_token = create_access_token(identity=str(user_id), expires_delta=timedelta(minutes=15))
        refresh_token = create_refresh_token(identity=user_id)
        
        # Mengatur masa berlaku untuk refresh token baru
        expires_at = datetime.utcnow() + timedelta(days=7)
        
        # Menghasilkan token refresh baru
        new_refresh_token = generate_token(db.session, user_id, refresh_token, expires_at)

        # Menambahkan log untuk aktivitas login
        add_log(db.session, user_id, "Pengguna Masuk", "Token dihasilkan.")
        
        try:
            db.session.commit()  # Menyimpan perubahan ke database
            
            # Membuat respons dengan token dan informasi pengguna
            response = make_response(
                jsonify(
                    {
                        "access_token": access_token,
                        "expires_at": expires_at.isoformat(),
                        "user": {
                            "id": user_id,
                            "full_name": full_name,
                            "email": user["email"],
                            "role": role
                        },
                    }
                )
            )
            
            # Mengatur cookie untuk refresh token
            response.set_cookie(
                "refresh_token",
                new_refresh_token.token,
                httponly=True,
                secure=True,
                samesite="None",
            )
            return response, 200
        except Exception as e:
            # Menggulung kembali sesi jika terjadi kesalahan
            db.session.rollback()
            return jsonify({"message": "Gagal untuk menyimpan token"}), 500
    else:
        return jsonify({"message": "Email atau kata sandi tidak valid"}), 401