from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User, createUser, updateUser, deleteUser
from ..middlewares.is_login import is_login
from ..middlewares.has_access import has_access
from ..models.refresh_token import RefreshToken
from ..models.log import Log, delete_log, add_log
from .. import db

users_bp = Blueprint("users_bp", __name__)


@users_bp.route("/users", methods=["POST"])
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu"])
def create_user():
    # Mengambil data JSON dari permintaan
    data = request.get_json()
    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")  # Mengatur peran default sebagai 'user'

    # Memeriksa apakah nama lengkap, email, dan kata sandi disediakan
    if not full_name or not email or not password:
        return jsonify({"message": "Nama lengkap, email, dan kata sandi diperlukan."}), 400

    try:
        # Membuat pengguna baru
        user = createUser(full_name, email, password, role)

        # Menambahkan log keberhasilan pembuatan pengguna
        user_id = get_jwt_identity()
        add_log(db.session, user_id, "Berhasil Buat Pengguna", f"Pengguna baru dibuat dengan nama {user.full_name}.")

        return jsonify(
            {
                "message": "Pengguna berhasil dibuat",
                "data": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "role": user.role,
                },
            }
        ), 201
    except Exception as e:
        return jsonify({"message": f"Kesalahan saat membuat pengguna: {str(e)}"}), 500


@users_bp.route("/users/<int:user_id>", methods=["PUT", "OPTIONS"])
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu"])
def update_user(user_id):
    # Mengambil data JSON dari permintaan
    data = request.get_json()
    user = User.query.get(user_id)  # Mencari pengguna berdasarkan ID
    if user:
        # Memperbarui pengguna dengan data baru
        updated_user = updateUser(user_id, data)
        if updated_user:
            # Menambahkan log keberhasilan pembaruan pengguna
            user_id = get_jwt_identity()
            add_log(db.session, user_id, "Berhasil Perbarui Pengguna", f"Pengguna ID {user_id} berhasil diperbarui.")

            return jsonify(
                {
                    "message": "Pengguna berhasil diperbarui",
                    "data": {
                        "id": updated_user.id,
                        "full_name": updated_user.full_name,
                        "email": updated_user.email,
                        "role": updated_user.role,
                    },
                }
            ), 200
        return jsonify({"message": "Gagal untuk memperbarui pengguna"}), 400
    return jsonify({"message": "Pengguna tidak ditemukan"}), 404


@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
@has_access(["super_admin"])
def delete_user(user_id):
    # Mencari pengguna berdasarkan ID
    user = User.query.get(user_id)
    
    if user:
        try:
            # Menghapus log terkait pengguna
            logs = Log.query.filter_by(user_id=user_id).all()
            for log in logs:
                delete_log(db.session, log.id)
            
            # Menghapus token refresh terkait pengguna
            RefreshToken.query.filter_by(user_id=user_id).delete()

            # Menghapus pengguna
            if deleteUser(user_id):
                # Menambahkan log keberhasilan penghapusan pengguna
                user_id = get_jwt_identity()
                add_log(db.session, user_id, "Berhasil Hapus Pengguna", f"Pengguna ID {user_id} berhasil dihapus.")

                return jsonify({"message": "Pengguna, token terkait, dan log berhasil dihapus"}), 200
            else:
                return jsonify({"message": "Gagal untuk menghapus pengguna"}), 400
        except Exception as e:
            return jsonify({"message": f"Gagal untuk menghapus pengguna: {str(e)}"}), 400
    
    return jsonify({"message": "Pengguna tidak ditemukan"}), 404


@users_bp.route("/users", methods=["GET"])
@jwt_required()
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu"])
def get_users():
    # Mengambil semua pengguna dari database
    users = User.query.all()
    users_list = [
        {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
        }
        for user in users
    ]
    return jsonify({"data": users_list}), 200


@users_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu"])
def get_user(user_id):
    # Mendapatkan ID pengguna dari token JWT
    current_user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user:
        return jsonify(
            {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role,
            }
        ), 200
    return jsonify({"message": "Pengguna tidak ditemukan"}), 404

