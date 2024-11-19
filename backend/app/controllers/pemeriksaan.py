from flask import Blueprint, request, jsonify
from ..models.pemeriksaan import Pemeriksaan
from ..middlewares.has_access import has_access
from ..services.check_stunting import check_stunting
from .. import db

pemeriksaan_bp = Blueprint("pemeriksaan_bp", __name__)


@pemeriksaan_bp.route("/pemeriksaan", methods=["POST"])
@has_access(["admin_posyandu"])
def create_pemeriksaan():
    data = request.get_json()
    anak_id = data.get("anak_id")
    date = data.get("date")

    if not anak_id or not date:
        return jsonify({"error": "Data tidak lengkap"}), 400

    result = check_stunting(anak_id)

    new_pemeriksaan = Pemeriksaan(anak_id=anak_id, date=date, result=result)

    db.session.add(new_pemeriksaan)
    db.session.commit()

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
@has_access(["admin_posyandu"])
def update_pemeriksaan(id):
    data = request.get_json()
    pemeriksaan = Pemeriksaan.query.get(id)

    if not pemeriksaan:
        return jsonify({"error": "Pemeriksaan tidak ditemukan"}), 404

    if "anak_id" in data:
        pemeriksaan.anak_id = data["anak_id"]
    if "date" in data:
        pemeriksaan.date = data["date"]
    if "result" in data:
        pemeriksaan.result = data["result"]

    db.session.commit()

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
@has_access(["admin_posyandu"])
def update_pemeriksaan_by_anak(anak_id):
    data = request.get_json()
    pemeriksaan_list = Pemeriksaan.query.filter_by(anak_id=anak_id).all()

    if not pemeriksaan_list:
        return jsonify({"error": "Pemeriksaan tidak ditemukan untuk anak_id tersebut"}), 404

    for pemeriksaan in pemeriksaan_list:
        if "date" in data:
            pemeriksaan.date = data["date"]
        if "result" in data:
            pemeriksaan.result = data["result"]

    db.session.commit()

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
@has_access(["admin_posyandu"])
def delete_pemeriksaan(id):
    pemeriksaan = Pemeriksaan.query.get(id)

    if not pemeriksaan:
        return jsonify({"error": "Pemeriksaan tidak ditemukan"}), 404

    db.session.delete(pemeriksaan)
    db.session.commit()

    return jsonify({"message": "Pemeriksaan berhasil dihapus"}), 200


@pemeriksaan_bp.route("/pemeriksaan/anak/<int:anak_id>", methods=["DELETE"])
@has_access(["admin_posyandu"])
def delete_pemeriksaan_by_anak(anak_id):
    pemeriksaan_list = Pemeriksaan.query.filter_by(anak_id=anak_id).all()

    if not pemeriksaan_list:
        return jsonify({"error": "Data pemeriksaan tidak ditemukan untuk anak_id tersebut"}), 404

    for pemeriksaan in pemeriksaan_list:
        db.session.delete(pemeriksaan)

    db.session.commit()

    return jsonify({"message": "Data pemeriksaan berhasil dihapus"}), 200


@pemeriksaan_bp.route("/pemeriksaan/anak/<int:anak_id>", methods=["GET"])
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_pemeriksaan_by_anak(anak_id):
    pemeriksaan_list = Pemeriksaan.query.filter_by(anak_id=anak_id).all()

    if not pemeriksaan_list:
        return jsonify({"error": "Data pemeriksaan anak tidak ditemukan"}), 404

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
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_all_pemeriksaan():
    pemeriksaan_list = Pemeriksaan.query.all()

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
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_pemeriksaan_by_id(id):
    pemeriksaan = Pemeriksaan.query.get(id)

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
        ]
    ), 200
