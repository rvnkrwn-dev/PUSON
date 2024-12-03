from flask import Blueprint, jsonify, request
from ..models.user import User, updateUser
from ..services.email_helper import send_email
from datetime import datetime, timedelta
from ..models.log import add_log
import secrets
from .. import db

forget_password_bp = Blueprint("password_reset", __name__)

@forget_password_bp.route("/forget-password", methods=["POST"])
def forget_password():
    # Mengambil email dari permintaan JSON
    email = request.json.get("email")
    user = User.query.filter_by(email=email).first()

    # Memeriksa apakah pengguna terdaftar
    if not user:
        return jsonify({"message": "Email tidak terdaftar"}), 404

    # Menghasilkan token reset
    token = secrets.token_urlsafe()
    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=24)

    # Memperbarui pengguna dengan token dan masa berlaku
    updateUser(
        user.id, {"reset_token": token, "reset_token_expiry": user.reset_token_expiry}
    )

    # Mengirim email permintaan reset kata sandi
    send_email(
        "Permintaan Reset Kata Sandi",
        f"""
        Yth. Pengguna,

        Kami menerima permintaan untuk mereset kata sandi Anda. Jika Anda yang melakukan permintaan ini, silakan klik tautan di bawah untuk mereset kata sandi Anda:

        {request.url_root}auth/reset-password/{token}

        Jika Anda tidak merasa melakukan permintaan ini, abaikan email ini atau hubungi tim dukungan kami jika ada kekhawatiran.

        Salam hangat,  
        Tim Dukungan PUSON
        """,
        email,
    )

    # Menambahkan log untuk aktivitas lupa sandi
    add_log(db.session, user.id, "Kirim URL Reset Kata Sandi", f"Berhasil membuat URL reset kata sandi untuk email {email} dan mengirimkan email.")
    
    return jsonify({"message": "Email reset kata sandi telah dikirim"}), 200
