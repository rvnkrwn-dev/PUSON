from flask import Blueprint, request, jsonify
from ..models import Pemeriksaan, Anak
from sqlalchemy.orm import joinedload
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..middlewares.is_login import is_login
from ..middlewares.has_access import has_access
from ..services.check_stunting import check_stunting
from ..models.log import add_log
from .. import db

pemeriksaan_bp = Blueprint("pemeriksaan_bp", __name__)


@pemeriksaan_bp.route("/pemeriksaan", methods=["POST"])
@jwt_required()
@is_login
@has_access(['super_admin', "admin_posyandu"])
def create_pemeriksaan():
    # Mengambil data JSON dari permintaan
    data = request.get_json()
    anak_id = data.get("anak_id")
    date = data.get("date")
    user_id = get_jwt_identity()  # Mendapatkan ID pengguna yang melakukan request (misal dari JWT)

    # Memeriksa apakah anak_id dan date disediakan
    if not anak_id or not date:
        return jsonify({"error": "Data tidak lengkap"}), 400

    # Memeriksa status stunting anak
    result = check_stunting(anak_id)

    # Membuat objek Pemeriksaan baru
    new_pemeriksaan = Pemeriksaan(anak_id=anak_id, date=date, result=result)

    try:
        # Menambahkan pemeriksaan baru ke sesi database
        db.session.add(new_pemeriksaan)
        db.session.commit()

        # Menambahkan log untuk aktivitas menambahkan data pemeriksaan
        add_log(db.session, user_id, "Tambah Data Pemeriksaan", f"Berhasil menambahkan data pemeriksaan untuk anak ID: {anak_id}.")

        # Mengembalikan respons dengan detail pemeriksaan yang baru dibuat
        return jsonify(
            {
                "id": new_pemeriksaan.id,
                "anak_id": new_pemeriksaan.anak_id,
                "date": new_pemeriksaan.date,
                "result": new_pemeriksaan.result,
                "created_at": new_pemeriksaan.created_at,
                "updated_at": new_pemeriksaan.updated_at,
            }
        ), 201
    except Exception as e:
        # Jika terjadi kesalahan saat menyimpan data ke database
        db.session.rollback()
        return jsonify({"error": "Terjadi kesalahan saat menambah data pemeriksaan"}), 500


@pemeriksaan_bp.route("/pemeriksaan/anak/<int:anak_id>", methods=["PUT"])
@jwt_required()
@is_login
@has_access(['super_admin', "admin_posyandu"])
def update_pemeriksaan_by_anak(anak_id):
    # Mengambil data JSON dari permintaan
    data = request.get_json()
    user_id = get_jwt_identity()  # Mendapatkan ID pengguna yang melakukan request (misal dari JWT)

    # Mencari semua pemeriksaan berdasarkan anak_id
    pemeriksaan_list = Pemeriksaan.query.filter_by(anak_id=anak_id).all()

    # Memeriksa apakah ada pemeriksaan untuk anak_id tersebut
    if not pemeriksaan_list:
        return jsonify({"error": "Pemeriksaan tidak ditemukan untuk anak_id tersebut"}), 404

    try:
        # Memperbarui atribut pemeriksaan dengan data baru
        for pemeriksaan in pemeriksaan_list:
            if "date" in data:
                pemeriksaan.date = data["date"]  # Memperbarui tanggal pemeriksaan
            if "result" in data:
                pemeriksaan.result = data["result"]  # Memperbarui hasil pemeriksaan

        # Menyimpan perubahan ke database
        db.session.commit()

        # Menambahkan log untuk aktivitas memperbarui data pemeriksaan
        add_log(db.session, user_id, "Perbarui Data Pemeriksaan by Anak", f"Berhasil memperbarui data pemeriksaan untuk anak_id: {anak_id}.")

        # Mengembalikan respons dengan daftar pemeriksaan yang diperbarui
        return jsonify(
            [
                {
                    "id": pemeriksaan.id,
                    "anak_id": pemeriksaan.anak_id,
                    "date": pemeriksaan.date,
                    "result": pemeriksaan.result,
                    "created_at": pemeriksaan.created_at,
                    "updated_at": pemeriksaan.updated_at,
                }
                for pemeriksaan in pemeriksaan_list
            ]
        ), 200
    except Exception as e:
        # Jika terjadi kesalahan saat menyimpan perubahan
        db.session.rollback()
        return jsonify({"error": "Terjadi kesalahan saat memperbarui data pemeriksaan"}), 500


@pemeriksaan_bp.route("/pemeriksaan/<int:id>", methods=["DELETE"])
@jwt_required()
@is_login
@has_access(['super_admin', "admin_posyandu"])
def delete_pemeriksaan(id):
    user_id = get_jwt_identity()  # Mendapatkan ID pengguna yang melakukan request (misal dari JWT)
    
    # Mencari pemeriksaan berdasarkan ID
    pemeriksaan = Pemeriksaan.query.get(id)

    # Memeriksa apakah pemeriksaan ditemukan
    if not pemeriksaan:
        return jsonify({"error": "Data pemeriksaan tidak ditemukan"}), 404

    try:
        # Menghapus pemeriksaan dari database
        db.session.delete(pemeriksaan)
        db.session.commit()

        # Menambahkan log untuk aktivitas menghapus data pemeriksaan
        add_log(db.session, user_id, "Hapus Data Pemeriksaan", f"Berhasil menghapus data pemeriksaan dengan ID {id}.")
        
        # Mengembalikan respons sukses
        return jsonify({"message": "Pemeriksaan berhasil dihapus"}), 200
    
    except Exception as e:
        # Jika terjadi kesalahan saat menghapus data
        db.session.rollback()
        return jsonify({"error": "Terjadi kesalahan saat menghapus data pemeriksaan"}), 500


@pemeriksaan_bp.route("/pemeriksaan/anak/<int:anak_id>", methods=["DELETE"])
@jwt_required()
@is_login
@has_access(['super_admin', "admin_posyandu"])
def delete_pemeriksaan_by_anak(anak_id):
    user_id = get_jwt_identity()  # Mendapatkan ID pengguna yang melakukan request (misal dari JWT)

    # Mencari semua pemeriksaan berdasarkan anak_id
    pemeriksaan_list = Pemeriksaan.query.filter_by(anak_id=anak_id).all()

    # Memeriksa apakah ada pemeriksaan untuk anak_id tersebut
    if not pemeriksaan_list:
        return jsonify({"error": "Data pemeriksaan tidak ditemukan untuk anak_id tersebut"}), 404

    try:
        # Menghapus setiap pemeriksaan yang ditemukan
        for pemeriksaan in pemeriksaan_list:
            db.session.delete(pemeriksaan)  # Menghapus pemeriksaan dari sesi

        # Menyimpan perubahan ke database
        db.session.commit()

        # Menambahkan log untuk aktivitas menghapus data pemeriksaan berdasarkan anak_id
        add_log(db.session, user_id, "Hapus Data Pemeriksaan", f"Berhasil menghapus data pemeriksaan untuk anak_id {anak_id}.")
        
        # Mengembalikan respons sukses setelah penghapusan
        return jsonify({"message": "Data pemeriksaan berhasil dihapus"}), 200

    except Exception as e:
        # Jika terjadi kesalahan saat menghapus data
        db.session.rollback()
        return jsonify({"error": "Terjadi kesalahan saat menghapus data pemeriksaan"}), 500


@pemeriksaan_bp.route("/pemeriksaan", methods=["GET"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_all_pemeriksaan():
    # Ambil query parameter untuk pagination dan filter
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    anak_id = request.args.get("anak_id", type=int)  # Filter berdasarkan anak_id

    # Query dasar untuk pemeriksaan dengan join ke tabel Anak
    query = db.session.query(Pemeriksaan, Anak).join(Anak, Pemeriksaan.anak_id == Anak.id)

    # Filter berdasarkan anak_id jika disediakan
    if anak_id:
        query = query.filter(Pemeriksaan.anak_id == anak_id)

    # Pagination
    pemeriksaan_paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    # Mengembalikan respons dengan data pemeriksaan dan metadata pagination
    return jsonify(
        {
            "data": [
                {
                    "id": pemeriksaan.id,
                    "anak_id": pemeriksaan.anak_id,
                    "nama_anak": anak.name,  # Nama anak yang diambil dari relasi
                    "date": pemeriksaan.date,
                    "result": pemeriksaan.result,
                    "created_at": pemeriksaan.created_at,
                    "updated_at": pemeriksaan.updated_at,
                }
                for pemeriksaan, anak in pemeriksaan_paginated.items  # Unpack tuple dari join
            ],
            "pagination": {
                "total": pemeriksaan_paginated.total,
                "page": pemeriksaan_paginated.page,
                "per_page": pemeriksaan_paginated.per_page,
                "total_pages": pemeriksaan_paginated.pages,
                "has_next_page": pemeriksaan_paginated.has_next,
                "has_previous_page": pemeriksaan_paginated.has_prev,
            },
        }
    ), 200


@pemeriksaan_bp.route("/pemeriksaan/<int:id>", methods=["GET"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_pemeriksaan_by_id(id):
    # Mencari pemeriksaan berdasarkan ID
    pemeriksaan = Pemeriksaan.query.get(id)
    # Memeriksa apakah pemeriksaan ditemukan
    if not pemeriksaan:
        return jsonify({"message": "Data pemeriksaan tidak ditemukan"}), 404
    # Mengembalikan respons dengan detail pemeriksaan yang ditemukan
    return jsonify(
        {
            "id": pemeriksaan.id,
            "anak_id": pemeriksaan.anak_id,
            "date": pemeriksaan.date,
            "result": pemeriksaan.result,
            "created_at": pemeriksaan.created_at,
            "updated_at": pemeriksaan.updated_at,
        }
    ), 200
