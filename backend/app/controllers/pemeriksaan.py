from flask import Blueprint, request, jsonify
from ..models.pemeriksaan import Pemeriksaan
from flask_jwt_extended import jwt_required
from ..middlewares.is_login import is_login
from ..middlewares.has_access import has_access
from ..services.check_stunting import check_stunting
from .. import db

pemeriksaan_bp = Blueprint("pemeriksaan_bp", __name__)


@pemeriksaan_bp.route("/pemeriksaan", methods=["POST"])
@jwt_required()
@is_login
@has_access(['super_admin',"admin_posyandu"])
def create_pemeriksaan():
    # Mengambil data JSON dari permintaan
    data = request.get_json()
    anak_id = data.get("anak_id")
    date = data.get("date")

    # Memeriksa apakah anak_id dan date disediakan
    if not anak_id or not date:
        return jsonify({"error": "Data tidak lengkap"}), 400

    # Memeriksa status stunting anak
    result = check_stunting(anak_id)

    # Membuat objek Pemeriksaan baru
    new_pemeriksaan = Pemeriksaan(anak_id=anak_id, date=date, result=result)

    # Menambahkan pemeriksaan baru ke sesi database
    db.session.add(new_pemeriksaan)
    db.session.commit()

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


@pemeriksaan_bp.route("/pemeriksaan/<int:id>", methods=["PUT"])
@jwt_required()
@is_login
@has_access(['super_admin',"admin_posyandu"])
def update_pemeriksaan(id):
    # Mengambil data JSON dari permintaan
    data = request.get_json()
    pemeriksaan = Pemeriksaan.query.get(id)

    # Memeriksa apakah pemeriksaan ditemukan
    if not pemeriksaan:
        return jsonify({"error": "Pemeriksaan tidak ditemukan"}), 404

    # Memperbarui atribut pemeriksaan dengan data baru
    if "anak_id" in data:
        pemeriksaan.anak_id = data["anak_id"]
    if "date" in data:
        pemeriksaan.date = data["date"]
    if "result" in data:
        pemeriksaan.result = data["result"]

    # Menyimpan perubahan ke database
    db.session.commit()

    # Mengembalikan respons dengan detail pemeriksaan yang diperbarui
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


@pemeriksaan_bp.route("/pemeriksaan/anak/<int:anak_id>", methods=["PUT"])
@jwt_required()
@is_login
@has_access(['super_admin',"admin_posyandu"])
def update_pemeriksaan_by_anak(anak_id):
    # Mengambil data JSON dari permintaan
    data = request.get_json()
    
    # Mencari semua pemeriksaan berdasarkan anak_id
    pemeriksaan_list = Pemeriksaan.query.filter_by(anak_id=anak_id).all()

    # Memeriksa apakah ada pemeriksaan untuk anak_id tersebut
    if not pemeriksaan_list:
        return jsonify({"error": "Pemeriksaan tidak ditemukan untuk anak_id tersebut"}), 404

    # Memperbarui atribut pemeriksaan dengan data baru
    for pemeriksaan in pemeriksaan_list:
        if "date" in data:
            pemeriksaan.date = data["date"]  # Memperbarui tanggal pemeriksaan
        if "result" in data:
            pemeriksaan.result = data["result"]  # Memperbarui hasil pemeriksaan

    # Menyimpan perubahan ke database
    db.session.commit()

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


@pemeriksaan_bp.route("/pemeriksaan/<int:id>", methods=["DELETE"])
@jwt_required()
@is_login
@has_access(['super_admin',"admin_posyandu"])
def delete_pemeriksaan(id):
    # Mencari pemeriksaan berdasarkan ID
    pemeriksaan = Pemeriksaan.query.get(id)

    # Memeriksa apakah pemeriksaan ditemukan
    if not pemeriksaan:
        return jsonify({"error": "Data pemeriksaan tidak ditemukan"}), 404

    # Menghapus pemeriksaan dari database
    db.session.delete(pemeriksaan)
    db.session.commit()

    # Mengembalikan respons sukses
    return jsonify({"message": "Pemeriksaan berhasil dihapus"}), 200


@pemeriksaan_bp.route("/pemeriksaan/anak/<int:anak_id>", methods=["DELETE"])
@jwt_required()
@is_login
@has_access(['super_admin',"admin_posyandu"])
def delete_pemeriksaan_by_anak(anak_id):
    # Mencari semua pemeriksaan berdasarkan anak_id
    pemeriksaan_list = Pemeriksaan.query.filter_by(anak_id=anak_id).all()

    # Memeriksa apakah ada pemeriksaan untuk anak_id tersebut
    if not pemeriksaan_list:
        return jsonify({"error": "Data pemeriksaan tidak ditemukan untuk anak_id tersebut"}), 404

    # Menghapus setiap pemeriksaan yang ditemukan
    for pemeriksaan in pemeriksaan_list:
        db.session.delete(pemeriksaan)  # Menghapus pemeriksaan dari sesi

    # Menyimpan perubahan ke database
    db.session.commit()

    # Mengembalikan respons sukses setelah penghapusan
    return jsonify({"message": "Data pemeriksaan berhasil dihapus"}), 200


@pemeriksaan_bp.route("/pemeriksaan/anak/<int:anak_id>", methods=["GET"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_pemeriksaan_by_anak(anak_id):
    # Mencari semua pemeriksaan berdasarkan anak_id
    pemeriksaan_list = Pemeriksaan.query.filter_by(anak_id=anak_id).all()

    # Memeriksa apakah ada pemeriksaan untuk anak_id tersebut
    if not pemeriksaan_list:
        return jsonify({"error": "Data pemeriksaan anak tidak ditemukan"}), 404

    # Mengembalikan respons dengan daftar pemeriksaan
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


@pemeriksaan_bp.route("/pemeriksaan", methods=["GET"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_all_pemeriksaan():
    # Mengambil semua data pemeriksaan dari database
    pemeriksaan_list = Pemeriksaan.query.all()

    # Mengembalikan respons dengan daftar semua pemeriksaan
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
