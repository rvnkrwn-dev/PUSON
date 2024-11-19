from flask import Blueprint, request, jsonify
from ..models import Anak
from ..middlewares.has_access import has_access
from .. import db

anak_bp = Blueprint("anak_bp", __name__)


@anak_bp.route("/anak", methods=["POST"])
@has_access(['admin_posyandu'])
def register_anak():
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    posyandu_id = data.get("posyandu_id")

    if not name or not age or not gender:
        return jsonify({"error": "Data tidak lengkap"}), 400

    new_anak = Anak(name=name, age=age, gender=gender, posyandu_id=posyandu_id)
    db.session.add(new_anak)
    db.session.commit()

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
@has_access(['admin_posyandu'])
def update_anak(id):
    data = request.get_json()
    anak = Anak.query.get(id)

    if not anak:
        return jsonify({"error": "Anak tidak ditemukan"}), 404

    for key, value in data.items():
        setattr(anak, key, value)

    db.session.commit()

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
@has_access(['admin_posyandu'])
def delete_anak(id):
    anak = Anak.query.get(id)

    if not anak:
        return jsonify({"error": "Anak tidak ditemukan"}), 404

    db.session.delete(anak)
    db.session.commit()

    return jsonify({"message": "Anak berhasil dihapus"}), 200


@anak_bp.route("/anak", methods=["GET"])
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_anak_list():
    anak_list = Anak.query.all()
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
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_anak_detail(id):
    anak = Anak.query.get(id)
    if not anak:
        return jsonify({"error": "Anak tidak ditemukan"}), 404

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
