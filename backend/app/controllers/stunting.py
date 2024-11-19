from flask import Blueprint, request, jsonify
from ..models.stunting import Stunting
from ..middlewares.has_access import has_access
from .. import db

stunting_bp = Blueprint("stunting_bp", __name__)


@stunting_bp.route("/stunting", methods=["POST"])
@has_access(['admin_posyandu'])
def add_stunting_data():
    data = request.get_json()
    anak_id = data.get("anak_id")
    date = data.get("date")
    height = data.get("height")
    weight = data.get("weight")

    if not anak_id or not date or not height or not weight:
        return jsonify({"error": "Data tidak lengkap"}), 400

    new_record = Stunting(
        anak_id=anak_id,
        date=date,
        height=height,
        weight=weight,
    )
    db.session.add(new_record)
    db.session.commit()

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
@has_access(['admin_posyandu'])
def update_stunting_data(id):
    data = request.get_json()
    stunting_record = Stunting.query.get(id)

    if not stunting_record:
        return jsonify({"error": "Data stunting tidak ditemukan"}), 404

    for key, value in data.items():
        setattr(stunting_record, key, value)

    db.session.commit()

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
@has_access(['admin_posyandu'])
def update_stunting_data_by_anak(anak_id):
    data = request.get_json()
    stunting_record = Stunting.query.filter_by(anak_id=anak_id).first()

    if not stunting_record:
        return jsonify({"error": "Data stunting tidak ditemukan"}), 404

    for key, value in data.items():
        setattr(stunting_record, key, value)

    db.session.commit()

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
@has_access(['admin_posyandu'])
def delete_stunting_data(id):
    stunting_record = Stunting.query.get(id)

    if not stunting_record:
        return jsonify({"error": "Data stunting tidak ditemukan"}), 404

    db.session.delete(stunting_record)
    db.session.commit()

    return jsonify({"message": "Data stunting berhasil dihapus"}), 200


@stunting_bp.route("/stunting/anak/<int:anak_id>", methods=["DELETE"])
@has_access(['admin_posyandu'])
def delete_stunting_data_by_anak(anak_id):
    stunting_records = Stunting.query.filter_by(anak_id=anak_id).all()

    if not stunting_records:
        return jsonify({"error": "Data stunting tidak ditemukan untuk anak_id tersebut"}), 404

    for record in stunting_records:
        db.session.delete(record)

    db.session.commit()

    return jsonify({"message": "Data stunting berhasil dihapus"}), 200


@stunting_bp.route("/stunting", methods=["GET"])
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_data():
    stunting_list = Stunting.query.all()
    return jsonify(
        [
            {
                "id": stunting.id,
                "anak_id": stunting.anak_id,
                "date": stunting.date,
                "height": stunting.height,
                "weight": stunting.weight,
                "created_at": stunting.created_at,
                "updated_at": stunting.updated_at,
            }
            for stunting in stunting_list
        ]
    ), 200


@stunting_bp.route("/stunting/anak/<int:anak_id>", methods=["GET"])
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_anak_data(anak_id):
    stunting_list = Stunting.query.filter_by(anak_id=anak_id).all()
    return jsonify(
        [
            {
                "id": stunting.id,
                "anak_id": stunting.anak_id,
                "date": stunting.date,
                "height": stunting.height,
                "weight": stunting.weight,
                "created_at": stunting.created_at,
                "updated_at": stunting.updated_at,
            }
            for stunting in stunting_list
        ]
    ), 200


@stunting_bp.route("/stunting/<int:id>", methods=["GET"])
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_stunting_detail(id):
    stunting_record = Stunting.query.get(id)
    if not stunting_record:
        return jsonify({"error": "Data stunting tidak ditemukan"}), 404

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
