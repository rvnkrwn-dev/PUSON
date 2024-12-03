from flask import Blueprint, request, jsonify
from ..models import Anak, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..middlewares.is_login import is_login
from ..middlewares.has_access import has_access
from sqlalchemy.orm import joinedload
from ..models.log import add_log
from .. import db

anak_bp = Blueprint("anak_bp", __name__)


@anak_bp.route("/anak", methods=["POST"])
@jwt_required()
@is_login
@has_access(['admin_posyandu'])
def register_anak():
    # Mendapatkan ID pengguna dari JWT
    user_id = get_jwt_identity()

    # Mengambil data JSON dari permintaan
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    posyandu_id = data.get("posyandu_id")

    # Memeriksa apakah data lengkap
    if not name or not age or not gender:
        return jsonify({"error": "Data tidak lengkap"}), 400

    # Membuat objek Anak baru
    new_anak = Anak(name=name, age=age, gender=gender, posyandu_id=posyandu_id)
    db.session.add(new_anak)  # Menambahkan objek Anak ke sesi
    db.session.commit()  # Menyimpan perubahan ke database
    
    # Menambahkan log untuk keberhasilan menambahkan data anak
    add_log(db.session, user_id, "Tambah Data Anak", f"Berhasil menambahkan data anak dengan nama {new_anak.name} (ID: {new_anak.id}).")
    
    # Mengembalikan respons dengan detail anak yang baru dibuat
    return jsonify(
        {
            "id": new_anak.id,
            "name": new_anak.name,
            "age": new_anak.age,
            "gender": new_anak.gender,
            "posyandu_id": new_anak.posyandu_id,
            "created_at": new_anak.created_at,
            "updated_at": new_anak.updated_at,
        }
    ), 201


@anak_bp.route("/anak/<int:id>", methods=["PUT"])
@jwt_required()
@is_login
@has_access(['admin_posyandu'])
def update_anak(id):
    # Mendapatkan ID pengguna dari JWT
    user_id = get_jwt_identity()

    # Mengambil data JSON dari permintaan
    data = request.get_json()
    anak = Anak.query.get(id)  # Mencari anak berdasarkan ID

    # Memeriksa apakah anak ditemukan
    if not anak:
        return jsonify({"error": "Anak tidak ditemukan"}), 404

    # Menyimpan nama anak sebelum diperbarui untuk log
    old_name = anak.name

    # Memperbarui atribut anak dengan data baru
    for key, value in data.items():
        setattr(anak, key, value)

    db.session.commit()  # Menyimpan perubahan ke database
    
    # Menambahkan log untuk berhasil memperbarui data anak
    add_log(db.session, user_id, "Berhasil Perbarui Data Anak", f"Berhasil memperbarui data anak {old_name} (ID: {anak.id}). Nama anak diperbarui menjadi {anak.name}.")
    
    # Mengembalikan respons dengan detail anak yang diperbarui
    return jsonify(
        {
            "id": anak.id,
            "name": anak.name,
            "age": anak.age,
            "gender": anak.gender,
            "posyandu_id": anak.posyandu_id,
            "created_at": anak.created_at,
            "updated_at": anak.updated_at,
        }
    ), 200


@anak_bp.route("/anak/<int:id>", methods=["DELETE"])
@jwt_required()
@is_login
@has_access(['admin_posyandu'])
def delete_anak(id):
    anak = Anak.query.get(id)  # Mencari anak berdasarkan ID
    # Mendapatkan ID pengguna dari JWT
    user_id = get_jwt_identity()

    # Memeriksa apakah anak ditemukan
    if not anak:
        return jsonify({"error": "Anak tidak ditemukan"}), 404

    db.session.delete(anak)  # Menghapus anak dari sesi
    db.session.commit()  # Menyimpan perubahan ke database
        
    # Menambahkan log untuk aktivitas menghapus data anak
    add_log(db.session, user_id=user_id, description=f"Berhasil menghapus data anak ID {id} dengan nama {anak.name}.")
    
    # Mengembalikan respons sukses setelah penghapusan
    return jsonify({"message": "Anak berhasil dihapus"}), 200


@anak_bp.route("/anak", methods=["GET"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_anak_list():
    # Ambil parameter halaman dan jumlah data per halaman dari query string
    page = request.args.get("page", 1, type=int)  # Default halaman 1
    per_page = request.args.get("per_page", 10, type=int)  # Default 10 data per halaman

    # Mengambil data anak dengan pagination
    anak_pagination = Anak.query.options(joinedload(Anak.posyandu)).paginate(page=page, per_page=per_page, error_out=False)

    # Data anak untuk halaman saat ini
    anak_list = anak_pagination.items

    # Membuat respons JSON
    return jsonify(
        {
            "data": [
                {
                    "id": anak.id,
                    "name": anak.name,
                    "age": anak.age,
                    "gender": anak.gender,
                    "posyandu_id": anak.posyandu_id,
                    "posyandu_name": anak.posyandu.name if anak.posyandu else None,
                    "created_at": anak.created_at,
                    "updated_at": anak.updated_at,
                }
                for anak in anak_list
            ],
            "pagination": {
                "total": anak_pagination.total,  # Total semua data
                "pages": anak_pagination.pages,  # Total halaman
                "current_page": anak_pagination.page,  # Halaman saat ini
                "per_page": anak_pagination.per_page,  # Jumlah data per halaman
                "has_next_page": anak_pagination.has_next,  # Apakah ada halaman berikutnya
                "has_previous_page": anak_pagination.has_prev,  # Apakah ada halaman sebelumnya
            },
        }
    ), 200


@anak_bp.route("/anak/<int:id>", methods=["GET"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_anak_detail(id):
    anak = Anak.query.get(id)  # Mencari anak berdasarkan ID
    
    # Memeriksa apakah anak ditemukan
    if not anak:
        return jsonify({"error": "Anak tidak ditemukan"}), 404

    # Mengembalikan respons dengan detail anak yang ditemukan
    return jsonify(
        {
            "id": anak.id,
            "name": anak.name,
            "age": anak.age,
            "gender": anak.gender,
            "posyandu_id": anak.posyandu_id,
            "created_at": anak.created_at,
            "updated_at": anak.updated_at,
        }
    ), 200
