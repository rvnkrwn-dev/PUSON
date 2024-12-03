from flask import Blueprint, request, jsonify
from ..models import Posyandu, Puskesmas
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..middlewares.is_login import is_login
from ..models.log import add_log
from ..middlewares.has_access import has_access
from sqlalchemy.orm import joinedload
from .. import db

posyandu_bp = Blueprint("posyandu_bp", __name__)


@posyandu_bp.route("/posyandu", methods=["POST"])
@jwt_required()
@is_login
@has_access(['admin_puskesmas'])
def create_posyandu():
    # Mengambil data JSON dari permintaan
    data = request.get_json()
    puskesmas_id = data.get("puskesmas_id")
    name = data.get("name")
    address = data.get("address")
    phone = data.get("phone")

    # Memeriksa apakah semua data yang diperlukan telah disediakan
    if not puskesmas_id or not name or not address or not phone:
        return jsonify({"error": "Data tidak lengkap"}), 400

    # Membuat objek Posyandu baru
    new_posyandu = Posyandu(
        puskesmas_id=puskesmas_id, name=name, address=address, phone=phone
    )
    db.session.add(new_posyandu)  # Menambahkan objek baru ke sesi
    db.session.commit()  # Menyimpan perubahan ke database

    # Menambahkan log untuk keberhasilan pembuatan posyandu
    user_id = get_jwt_identity()
    add_log(db.session, user_id, "Berhasil Buat Posyandu", f"Posyandu baru dengan nama {new_posyandu.name} berhasil dibuat.")

    # Mengembalikan respons dengan detail posyandu yang baru dibuat
    return jsonify(
        {
            "id": new_posyandu.id,
            "puskesmas_id": new_posyandu.puskesmas_id,
            "name": new_posyandu.name,
            "address": new_posyandu.address,
            "phone": new_posyandu.phone,
            "created_at": new_posyandu.created_at,
            "updated_at": new_posyandu.updated_at,
        }
    ), 201


@posyandu_bp.route("/posyandu/<int:id>", methods=["PUT"])
@jwt_required()
@is_login
@has_access(['admin_puskesmas'])
def update_posyandu(id):
    # Mengambil data JSON dari permintaan
    data = request.get_json()
    posyandu = Posyandu.query.get(id)  # Mencari posyandu berdasarkan ID

    # Memeriksa apakah posyandu ditemukan
    if not posyandu:
        return jsonify({"error": "Posyandu tidak ditemukan"}), 404

    # Menyimpan nama posyandu lama sebelum diperbarui
    old_name = posyandu.name

    # Memperbarui atribut posyandu dengan data baru
    for key, value in data.items():
        setattr(posyandu, key, value)

    db.session.commit()  # Menyimpan perubahan ke database

    # Menambahkan log untuk keberhasilan pembaruan posyandu
    user_id = get_jwt_identity()
    add_log(db.session, user_id, "Berhasil Perbarui Posyandu", f"Posyandu ID {id} ({old_name}) berhasil diperbarui menjadi {posyandu.name}.")

    # Mengembalikan respons dengan detail posyandu yang diperbarui
    return jsonify(
        {
            "id": posyandu.id,
            "puskesmas_id": posyandu.puskesmas_id,
            "name": posyandu.name,
            "address": posyandu.address,
            "phone": posyandu.phone,
            "created_at": posyandu.created_at,
            "updated_at": posyandu.updated_at,
        }
    ), 200


@posyandu_bp.route("/posyandu/<int:id>", methods=["DELETE"])
@jwt_required()
@is_login
@has_access(['admin_puskesmas'])
def delete_posyandu(id):
    # Mencari posyandu berdasarkan ID
    posyandu = Posyandu.query.get(id)

    # Memeriksa apakah posyandu ditemukan
    if not posyandu:
        return jsonify({"error": "Posyandu tidak ditemukan"}), 404

    db.session.delete(posyandu)  # Menghapus posyandu dari sesi
    db.session.commit()  # Menyimpan perubahan ke database

    # Menambahkan log untuk keberhasilan penghapusan posyandu
    user_id = get_jwt_identity()
    add_log(db.session, user_id, "Berhasil Hapus Posyandu", f"Posyandu ID {id} dengan nama {posyandu.name} berhasil dihapus.")

    # Mengembalikan respons sukses setelah penghapusan
    return jsonify({"message": "Posyandu berhasil dihapus"}), 200


@posyandu_bp.route("/posyandu", methods=["GET"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_posyandu_list():
    # Mendapatkan parameter `page` dan `per_page` dari query string
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    
    # Query posyandu dengan pagination
    posyandu_pagination = Posyandu.query.paginate(page=page, per_page=per_page, error_out=False)

    # Hasil data dalam format JSON
    posyandu_data = [
        {
            "id": posyandu.id,
            "puskesmas_id": posyandu.puskesmas_id,
            "name": posyandu.name,
            "address": posyandu.address,
            "phone": posyandu.phone,
            "created_at": posyandu.created_at,
            "updated_at": posyandu.updated_at,
        }
        for posyandu in posyandu_pagination.items
    ]

    # Mengembalikan respons JSON
    return jsonify({
        "data": posyandu_data,
        "meta": {
            "current_page": posyandu_pagination.page,
            "per_page": posyandu_pagination.per_page,
            "total_items": posyandu_pagination.total,
            "total_pages": posyandu_pagination.pages,
            "has_next_page": posyandu_pagination.has_next,
            "has_previous_page": posyandu_pagination.has_prev,
        }
    }), 200


@posyandu_bp.route("/posyandu/<int:id>", methods=["GET"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_posyandu_detail(id):
    # Mencari posyandu berdasarkan ID
    posyandu = Posyandu.query.get(id)
    
    # Memeriksa apakah posyandu ditemukan
    if not posyandu:
        return jsonify({"error": "Posyandu tidak ditemukan"}), 404

    # Mengembalikan respons dengan detail posyandu yang ditemukan
    return jsonify(
        {
            "id": posyandu.id,
            "puskesmas_id": posyandu.puskesmas_id,
            "name": posyandu.name,
            "address": posyandu.address,
            "phone": posyandu.phone,
            "created_at": posyandu.created_at,
            "updated_at": posyandu.updated_at,
        }
    ), 200
