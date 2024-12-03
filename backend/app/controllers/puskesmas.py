from flask import Blueprint, request, jsonify
from ..models.puskesmas import Puskesmas
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..middlewares.is_login import is_login
from ..models.log import add_log
from ..middlewares.has_access import has_access
from .. import db

puskesmas_bp = Blueprint("puskesmas", __name__)


@puskesmas_bp.route("/puskesmas", methods=["POST"])
@jwt_required()
@is_login
@has_access(['super_admin', 'admin_puskesmas'])
def create():
    # Mengambil ID pengguna dari JWT
    user_id = get_jwt_identity()

    # Mengambil data JSON dari permintaan
    data = request.get_json()
    
    # Memeriksa apakah data yang diperlukan ada
    if not data or not all(key in data for key in ("name", "address", "phone")):
        return jsonify({"message": "Input tidak valid"}), 400

    # Membuat objek Puskesmas baru
    new_puskesmas = Puskesmas(
        name=data["name"], address=data["address"], phone=data["phone"]
    )
    db.session.add(new_puskesmas)  # Menambahkan objek baru ke sesi
    db.session.commit()  # Menyimpan perubahan ke database

    # Menambahkan log untuk keberhasilan pembuatan data Puskesmas
    add_log(db.session, user_id, "Berhasil Buat Data Puskesmas", f"Puskesmas baru dibuat dengan nama {new_puskesmas.name}.")

    # Mengembalikan respons dengan detail puskesmas yang baru dibuat
    return jsonify(
        {
            "id": new_puskesmas.id,
            "name": new_puskesmas.name,
            "address": new_puskesmas.address,
            "phone": new_puskesmas.phone,
            "created_at": new_puskesmas.created_at,
            "updated_at": new_puskesmas.updated_at,
        }
    ), 201

@puskesmas_bp.route("/puskesmas/<int:id>", methods=["PUT"])
@jwt_required()
@is_login
@has_access(['super_admin', 'admin_puskesmas'])
def update(id):
    # Mengambil ID pengguna dari JWT
    user_id = get_jwt_identity()

    # Mengambil data JSON dari permintaan
    data = request.get_json()
    
    # Memeriksa apakah data ada
    if not data:
        return jsonify({"message": "Input tidak valid"}), 400

    # Mencari puskesmas berdasarkan ID
    puskesmas = Puskesmas.query.get(id)
    
    # Memeriksa apakah puskesmas ditemukan
    if not puskesmas:
        return jsonify({"message": "Puskesmas tidak ditemukan"}), 404

    # Menyimpan nama puskesmas lama sebelum diperbarui
    old_name = puskesmas.name

    # Memperbarui atribut puskesmas dengan data baru
    if "name" in data:
        puskesmas.name = data["name"]
    if "address" in data:
        puskesmas.address = data["address"]
    if "phone" in data:
        puskesmas.phone = data["phone"]

    db.session.commit()  # Menyimpan perubahan ke database

    # Menambahkan log untuk keberhasilan memperbarui data puskesmas
    add_log(db.session, user_id, "Berhasil Perbarui Data Puskesmas", f"Puskesmas ID {id} ({old_name}) berhasil diperbarui menjadi {puskesmas.name}.")

    # Mengembalikan respons dengan detail puskesmas yang diperbarui
    return jsonify(
        {
            "id": puskesmas.id,
            "name": puskesmas.name,
            "address": puskesmas.address,
            "phone": puskesmas.phone,
            "created_at": puskesmas.created_at,
            "updated_at": puskesmas.updated_at,
        }
    ), 200


@puskesmas_bp.route("/puskesmas/<int:id>", methods=["DELETE"])
@jwt_required()
@is_login
@has_access(['super_admin', 'admin_puskesmas'])
def delete(id):
    # Mengambil ID pengguna dari JWT
    user_id = get_jwt_identity()

    # Mencari puskesmas berdasarkan ID
    puskesmas = Puskesmas.query.get(id)
    
    # Memeriksa apakah puskesmas ditemukan
    if not puskesmas:
        return jsonify({"message": "Puskesmas tidak ditemukan"}), 404

    db.session.delete(puskesmas)  # Menghapus puskesmas dari sesi
    db.session.commit()  # Menyimpan perubahan ke database

    # Menambahkan log untuk keberhasilan penghapusan puskesmas
    add_log(db.session, user_id, "Berhasil Hapus Data Puskesmas", f"Puskesmas ID {id} dengan nama {puskesmas.name} berhasil dihapus.")

    # Mengembalikan respons sukses setelah penghapusan
    return jsonify({"message": "Puskesmas berhasil dihapus"}), 200


@puskesmas_bp.route("/puskesmas", methods=["GET"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_puskesmas_list():
    # Ambil parameter halaman dan jumlah data per halaman dari query string
    page = request.args.get("page", 1, type=int)  # Default halaman 1
    per_page = request.args.get("per_page", 10, type=int)  # Default 10 data per halaman

    # Mengambil data puskesmas dengan pagination
    puskesmas_pagination = Puskesmas.query.paginate(page=page, per_page=per_page, error_out=False)

    # Data puskesmas untuk halaman saat ini
    puskesmas_list = puskesmas_pagination.items

    # Mengembalikan respons dengan detail puskesmas yang ditemukan dan informasi pagination
    return jsonify(
        {
            "data": [
                {
                    "id": puskesmas.id,
                    "name": puskesmas.name,
                    "address": puskesmas.address,
                    "phone": puskesmas.phone,
                    "created_at": puskesmas.created_at,
                    "updated_at": puskesmas.updated_at,
                } for puskesmas in puskesmas_list
            ],
            "pagination": {
                "total": puskesmas_pagination.total,  # Total semua data
                "pages": puskesmas_pagination.pages,  # Total halaman
                "current_page": puskesmas_pagination.page,  # Halaman saat ini
                "per_page": puskesmas_pagination.per_page,  # Jumlah data per halaman
                "has_next_page": puskesmas_pagination.has_next,  # Apakah ada halaman berikutnya
                "has_previous_page": puskesmas_pagination.has_prev,  # Apakah ada halaman sebelumnya
                "next_page": puskesmas_pagination.next_num if puskesmas_pagination.has_next else None,
                "previous_page": puskesmas_pagination.prev_num if puskesmas_pagination.has_prev else None
            }
        }
    ), 200
