from flask import Blueprint, request, jsonify
from ..models.posyandu import Posyandu
from ..middlewares.has_access import has_access
from .. import db

posyandu_bp = Blueprint("posyandu_bp", __name__)


@posyandu_bp.route("/posyandu", methods=["POST"])
@has_access(['admin_puskesmas'])
def create_posyandu():
    data = request.get_json()
    puskesmas_id = data.get("puskesmas_id")
    name = data.get("name")
    address = data.get("address")
    phone = data.get("phone")

    if not puskesmas_id or not name or not address or not phone:
        return jsonify({"error": "Data tidak lengkap"}), 400

    new_posyandu = Posyandu(
        puskesmas_id=puskesmas_id, name=name, address=address, phone=phone
    )
    db.session.add(new_posyandu)
    db.session.commit()

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
@has_access(['admin_puskesmas'])
def update_posyandu(id):
    data = request.get_json()
    posyandu = Posyandu.query.get(id)

    if not posyandu:
        return jsonify({"error": "Posyandu tidak ditemukan"}), 404

    for key, value in data.items():
        setattr(posyandu, key, value)

    db.session.commit()

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
@has_access(['admin_puskesmas'])
def delete_posyandu(id):
    posyandu = Posyandu.query.get(id)

    if not posyandu:
        return jsonify({"error": "Posyandu tidak ditemukan"}), 404

    db.session.delete(posyandu)
    db.session.commit()

    return jsonify({"message": "Posyandu berhasil dihapus"}), 200


@posyandu_bp.route("/posyandu", methods=["GET"])
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_posyandu_list():
    posyandu_list = Posyandu.query.all()
    return jsonify(
        [
            {
                "id": posyandu.id,
                "puskesmas_id": posyandu.puskesmas_id,
                "name": posyandu.name,
                "address": posyandu.address,
                "phone": posyandu.phone,
                "created_at": posyandu.created_at,
                "updated_at": posyandu.updated_at,
            }
            for posyandu in posyandu_list
        ]
    ), 200


@posyandu_bp.route("/posyandu/<int:id>", methods=["GET"])
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_posyandu_detail(id):
    posyandu = Posyandu.query.get(id)
    if not posyandu:
        return jsonify({"error": "Posyandu tidak ditemukan"}), 404

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
