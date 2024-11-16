from flask import Blueprint, request, jsonify
from ..models.pemeriksaan import Pemeriksaan
from ..middlewares.has_access import has_access
from .. import db

pemeriksaan_bp = Blueprint("pemeriksaan_bp", __name__)


@pemeriksaan_bp.route("/pemeriksaan", methods=["POST"])
@has_access(['admin_posyandu'])
def create_pemeriksaan():
    data = request.get_json()
    anak_id = data.get("anak_id")
    date = data.get("date")
    result = data.get("result")

    if not anak_id or not date or not result:
        return jsonify({"error": "Data tidak lengkap"}), 400

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
@has_access(['admin_posyandu'])
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


@pemeriksaan_bp.route("/pemeriksaan/<int:id>", methods=["DELETE"])
@has_access(['admin_posyandu'])
def delete_pemeriksaan(id):
    pemeriksaan = Pemeriksaan.query.get(id)

    if not pemeriksaan:
        return jsonify({"error": "Pemeriksaan tidak ditemukan"}), 404

    db.session.delete(pemeriksaan)
    db.session.commit()

    return jsonify({"message": "Pemeriksaan berhasil dihapus"}), 200


@pemeriksaan_bp.route("/pemeriksaan/anak/<int:anak_id>", methods=["GET"])
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_pemeriksaan_by_anak(anak_id):
    pemeriksaan_list = Pemeriksaan.query.filter_by(anak_id=anak_id).all()
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
