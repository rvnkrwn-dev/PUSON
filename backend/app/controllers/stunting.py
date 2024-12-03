from flask import Blueprint, request, jsonify
from ..models import Stunting, Anak
from sqlalchemy.orm import joinedload
from ..models.log import add_log
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..middlewares.is_login import is_login
from ..middlewares.has_access import has_access
from .. import db

stunting_bp = Blueprint("stunting_bp", __name__)


@stunting_bp.route("/stunting", methods=["POST"])
@jwt_required()
@is_login
@has_access(['admin_posyandu'])
def add_stunting_data():
    # Mengambil ID pengguna dari JWT
    user_id = get_jwt_identity()

    # Mengambil data JSON dari permintaan
    data = request.get_json()
    anak_id = data.get("anak_id")
    date = data.get("date")
    height = data.get("height")
    weight = data.get("weight")

    # Memeriksa apakah semua data yang diperlukan telah disediakan
    if not anak_id or not date or not height or not weight:
        return jsonify({"error": "Data tidak lengkap"}), 400

    # Membuat catatan stunting baru
    new_record = Stunting(
        anak_id=anak_id,
        date=date,
        height=height,
        weight=weight,
    )
    db.session.add(new_record)  # Menambahkan catatan baru ke sesi
    db.session.commit()  # Menyimpan perubahan ke database

    # Menambahkan log untuk keberhasilan menambahkan data stunting
    add_log(db.session, user_id, "Berhasil Tambah Data Stunting", f"Stunting untuk anak_id {anak_id} berhasil ditambahkan.")

    # Mengembalikan respons dengan detail catatan stunting yang baru dibuat
    return jsonify(
        {
            "id": new_record.id,
            "anak_id": new_record.anak_id,
            "date": new_record.date,
            "height": new_record.height,
            "weight": new_record.weight,
            "created_at": new_record.created_at,
            "updated_at": new_record.updated_at,
        }
    ), 201


@stunting_bp.route("/stunting/<int:id>", methods=["PUT"])
@jwt_required()
@is_login
@has_access(['admin_posyandu'])
def update_stunting_data(id):
    # Mengambil ID pengguna dari JWT
    user_id = get_jwt_identity()

    # Mengambil data JSON dari permintaan
    data = request.get_json()
    stunting_record = Stunting.query.get(id)  # Mencari catatan stunting berdasarkan ID

    # Memeriksa apakah catatan stunting ditemukan
    if not stunting_record:
        return jsonify({"error": "Data stunting tidak ditemukan"}), 404

    # Memperbarui atribut catatan stunting dengan data baru
    for key, value in data.items():
        setattr(stunting_record, key, value)

    db.session.commit()  # Menyimpan perubahan ke database

    # Menambahkan log untuk keberhasilan pembaruan data stunting
    add_log(db.session, user_id, "Berhasil Perbarui Data Stunting", f"Stunting untuk anak_id {stunting_record.anak_id} berhasil diperbarui.")

    # Mengembalikan respons dengan detail catatan stunting yang diperbarui
    return jsonify(
        {
            "id": stunting_record.id,
            "anak_id": stunting_record.anak_id,
            "date": stunting_record.date,
            "height": stunting_record.height,
            "weight": stunting_record.weight,
            "created_at": stunting_record.created_at,
            "updated_at": stunting_record.updated_at,
        }
    ), 200


@stunting_bp.route("/stunting/anak/<int:anak_id>", methods=["PUT"])
@jwt_required()
@is_login
@has_access(['admin_posyandu'])
def update_stunting_data_by_anak(anak_id):
    # Mengambil ID pengguna dari JWT
    user_id = get_jwt_identity()

    # Mengambil data JSON dari permintaan
    data = request.get_json()
    stunting_record = Stunting.query.filter_by(anak_id=anak_id).first()  # Mencari catatan stunting berdasarkan anak_id

    # Memeriksa apakah catatan stunting ditemukan
    if not stunting_record:
        return jsonify({"error": "Data stunting tidak ditemukan"}), 404

    # Memperbarui atribut catatan stunting dengan data baru
    for key, value in data.items():
        setattr(stunting_record, key, value)

    db.session.commit()  # Menyimpan perubahan ke database

    # Menambahkan log untuk keberhasilan pembaruan data stunting
    add_log(db.session, user_id, "Berhasil Perbarui Data Stunting", f"Stunting untuk anak_id {anak_id} berhasil diperbarui.")

    # Mengembalikan respons dengan detail catatan stunting yang diperbarui
    return jsonify(
        {
            "id": stunting_record.id,
            "anak_id": stunting_record.anak_id,
            "date": stunting_record.date,
            "height": stunting_record.height,
            "weight": stunting_record.weight,
            "created_at": stunting_record.created_at,
            "updated_at": stunting_record.updated_at,
        }
    ), 200


@stunting_bp.route("/stunting/<int:id>", methods=["DELETE"])
@jwt_required()
@is_login
@has_access(['admin_posyandu'])
def delete_stunting_data(id):
    # Mengambil ID pengguna dari JWT
    user_id = get_jwt_identity()

    # Mencari catatan stunting berdasarkan ID
    stunting_record = Stunting.query.get(id)

    # Memeriksa apakah catatan stunting ditemukan
    if not stunting_record:
        return jsonify({"error": "Data stunting tidak ditemukan"}), 404

    db.session.delete(stunting_record)  # Menghapus catatan stunting dari sesi
    db.session.commit()  # Menyimpan perubahan ke database

    # Menambahkan log untuk keberhasilan penghapusan data stunting
    add_log(db.session, user_id, "Berhasil Hapus Data Stunting", f"Stunting dengan id {id} berhasil dihapus.")

    # Mengembalikan respons sukses setelah penghapusan
    return jsonify({"message": "Data stunting berhasil dihapus"}), 200


@stunting_bp.route("/stunting/anak/<int:anak_id>", methods=["DELETE"])
@jwt_required()
@is_login
@has_access(['admin_posyandu'])
def delete_stunting_data_by_anak(anak_id):
    # Mengambil ID pengguna dari JWT
    user_id = get_jwt_identity()

    # Mencari semua catatan stunting berdasarkan anak_id
    stunting_records = Stunting.query.filter_by(anak_id=anak_id).all()

    # Memeriksa apakah ada catatan stunting untuk anak_id tersebut
    if not stunting_records:
        return jsonify({"error": "Data stunting tidak ditemukan untuk anak_id tersebut"}), 404

    # Menghapus setiap catatan stunting yang ditemukan
    for record in stunting_records:
        db.session.delete(record)

    db.session.commit()  # Menyimpan perubahan ke database

    # Menambahkan log untuk keberhasilan penghapusan data stunting
    add_log(db.session, user_id, "Berhasil Hapus Data Stunting", f"Semua data stunting untuk anak_id {anak_id} berhasil dihapus.")

    # Mengembalikan respons sukses setelah penghapusan
    return jsonify({"message": "Data stunting berhasil dihapus"}), 200


@stunting_bp.route("/stunting", methods=["GET"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_data():
    # Ambil query parameter untuk pagination
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    
    # Ambil query parameter untuk filter berdasarkan anak_id
    anak_id = request.args.get("anak_id", None, type=int)

    # Query dasar untuk stunting
    query = Stunting.query

    # Filter berdasarkan anak_id jika diberikan
    if anak_id:
        query = query.filter_by(anak_id=anak_id)

    # Pagination
    stunting_paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    # Mengembalikan respons dengan data stunting dan metadata pagination
    return jsonify(
        {
            "data": [
                {
                    "id": stunting.id,
                    "anak_id": stunting.anak_id,
                    "anak_name": stunting.anak.name,
                    "date": stunting.date,
                    "height": stunting.height,
                    "weight": stunting.weight,
                    "created_at": stunting.created_at,
                    "updated_at": stunting.updated_at,
                }
                for stunting in stunting_paginated.items
            ],
            "pagination": {
                "total": stunting_paginated.total,
                "page": stunting_paginated.page,
                "per_page": stunting_paginated.per_page,
                "total_pages": stunting_paginated.pages,
                "has_next_page": stunting_paginated.has_next,
                "has_previous_page": stunting_paginated.has_prev,
            },
        }
    ), 200


@stunting_bp.route("/stunting/<int:id>", methods=["GET"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_stunting_detail(id):
    # Mencari catatan stunting berdasarkan ID
    stunting_record = Stunting.query.get(id)
    
    # Memeriksa apakah catatan stunting ditemukan
    if not stunting_record:
        return jsonify({"error": "Data stunting tidak ditemukan"}), 404

    # Mengembalikan respons dengan detail catatan stunting yang ditemukan
    return jsonify(
        {
            "id": stunting_record.id,
            "anak_id": stunting_record.anak_id,
            "date": stunting_record.date,
            "height": stunting_record.height,
            "weight": stunting_record.weight,
            "created_at": stunting_record.created_at,
            "updated_at": stunting_record.updated_at,
        }
    ), 200
