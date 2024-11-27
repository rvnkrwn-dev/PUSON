from flask import Blueprint, request, jsonify
from ..models.user import User, createUser
from ..services.email_helper import send_email
import logging
from .. import db

register_bp = Blueprint("register", __name__)
logging.basicConfig(level=logging.DEBUG)


@register_bp.route("/register", methods=["POST"])
def register():
    # Mengambil data JSON dari permintaan
    data = request.get_json()
    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")  # Mengatur peran default sebagai 'user'

    # Memeriksa apakah semua data yang diperlukan telah disediakan
    if not all([full_name, email, password, role]):
        return jsonify({"message": "Data tidak lengkap"}), 400

    # Memeriksa apakah email sudah terdaftar
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email sudah terdaftar"}), 400

    try:
        # Membuat pengguna baru
        new_user = createUser(
            full_name=full_name, email=email, password=password, role=role
        )
        
        # Mengirim email selamat datang
        send_email(
            "Selamat Datang di Puson!",
            f"""
            Hai, {full_name}
            
            Terima kasih telah mendaftar di Puson! Kami sangat senang menyambut Anda ke dalam komunitas kami.
        
            Pendaftaran Anda telah berhasil. Proses persetujuan oleh tim kami telah selesai.
        
            Jika Anda memiliki pertanyaan atau membutuhkan bantuan, jangan ragu untuk menghubungi kami dengan reply atau melalui website puson.
        
            Salam hangat,  
            Tim Puson  
            """,
            email
        )

        logging.info(f"Registered user: {new_user.email}")
        # Mengembalikan respons sukses setelah pendaftaran
        return jsonify({"message": "Pendaftaran berhasil."}), 201
    except Exception as e:
        db.session.rollback()  # Menggulung kembali sesi jika terjadi kesalahan
        logging.error(f"Gagal untuk mendaftar pengguna: {e}")
        return jsonify({"message": "Gagal untuk mendaftar pengguna"}), 500
