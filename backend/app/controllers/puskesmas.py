from flask import Blueprint, request, jsonify
from ..models.puskesmas import Puskesmas
from flask_jwt_extended import jwt_required
from ..middlewares.is_login import is_login
from ..middlewares.has_access import has_access
from .. import db

puskesmas_bp = Blueprint("puskesmas", __name__)


@puskesmas_bp.route("/puskesmas", methods=["POST"])
@jwt_required()
@is_login
@has_access(['super_admin', 'admin_puskesmas'])
def create():
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


@puskesmas_bp.route("/puskesmas", methods=["GET"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_all():
    # Mengambil semua puskesmas dari database
    puskesmas_list = Puskesmas.query.all()
    return jsonify(
        [
            {
                "id": puskesmas.id,
                "name": puskesmas.name,
                "address": puskesmas.address,
                "phone": puskesmas.phone,
                "created_at": puskesmas.created_at,
                "updated_at": puskesmas.updated_at,
            }
            for puskesmas in puskesmas_list
        ]
    ), 200


@puskesmas_bp.route("/puskesmas/<int:id>", methods=["GET"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_puskesmas_detail(id):
    # Mencari puskesmas berdasarkan ID
    puskesmas = Puskesmas.query.get(id)
    
    # Memeriksa apakah puskesmas ditemukan
    if not puskesmas:
        return jsonify({"error": "Puskesmas tidak ditemukan"}), 404

    # Mengembalikan respons dengan detail puskesmas yang ditemukan
    return jsonify(
        [
            {
                "id": puskesmas.id,
                "name": puskesmas.name,
                "address": puskesmas.address,
                "phone": puskesmas.phone,
                "created_at": puskesmas.created_at,
                "updated_at": puskesmas.updated_at,
            }
        ]
    ), 200


@puskesmas_bp.route("/puskesmas/<int:id>", methods=["PUT"])
@jwt_required()
@is_login
@has_access(['super_admin', 'admin_puskesmas'])
def update(id):
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

    # Memperbarui atribut puskesmas dengan data baru
    if "name" in data:
        puskesmas.name = data["name"]
    if "address" in data:
        puskesmas.address = data["address"]
    if "phone" in data:
        puskesmas.phone = data["phone"]

    db.session.commit()  # Menyimpan perubahan ke database

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
    # Mencari puskesmas berdasarkan ID
    puskesmas = Puskesmas.query.get(id)
    
    # Memeriksa apakah puskesmas ditemukan
    if not puskesmas:
        return jsonify({"message": "Puskesmas tidak ditemukan"}), 404

    db.session.delete(puskesmas)  # Menghapus puskesmas dari sesi
    db.session.commit()  # Menyimpan perubahan ke database

    # Mengembalikan respons sukses setelah penghapusan
    return jsonify({"message": "Puskesmas berhasil dihapus"}), 200

