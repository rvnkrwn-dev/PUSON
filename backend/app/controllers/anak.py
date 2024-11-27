from flask import Blueprint, request, jsonify
from ..models import Anak
from flask_jwt_extended import jwt_required
from ..middlewares.is_login import is_login
from ..middlewares.has_access import has_access
from .. import db

anak_bp = Blueprint("anak_bp", __name__)


@anak_bp.route("/anak", methods=["POST"])
@jwt_required()
@is_login
@has_access(['admin_posyandu'])
def register_anak():
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
    # Mengambil data JSON dari permintaan
    data = request.get_json()
    anak = Anak.query.get(id)  # Mencari anak berdasarkan ID

    # Memeriksa apakah anak ditemukan
    if not anak:
        return jsonify({"error": "Anak tidak ditemukan"}), 404

    # Memperbarui atribut anak dengan data baru
    for key, value in data.items():
        setattr(anak, key, value)

    db.session.commit()  # Menyimpan perubahan ke database

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

    # Memeriksa apakah anak ditemukan
    if not anak:
        return jsonify({"error": "Anak tidak ditemukan"}), 404

    db.session.delete(anak)  # Menghapus anak dari sesi
    db.session.commit()  # Menyimpan perubahan ke database

    # Mengembalikan respons sukses setelah penghapusan
    return jsonify({"message": "Anak berhasil dihapus"}), 200


@anak_bp.route("/anak", methods=["GET"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_anak_list():
    anak_list = Anak.query.all()  # Mengambil semua anak dari database
    return jsonify(
        [
            {
                "id": anak.id,
                "name": anak.name,
                "age": anak.age,
                "gender": anak.gender,
                "posyandu_id": anak.posyandu_id,
                "created_at": anak.created_at,
                "updated_at": anak.updated_at,
            }
            for anak in anak_list
        ]
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
