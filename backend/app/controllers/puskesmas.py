from flask import Blueprint, request, jsonify
from ..models.puskesmas import Puskesmas
from ..middlewares.has_access import has_access
from .. import db

puskesmas_bp = Blueprint("puskesmas", __name__)


@puskesmas_bp.route("/puskesmas", methods=["POST"])
@has_access(['super_admin', 'admin_puskesmas'])
def create():
    data = request.get_json()
    if not data or not all(key in data for key in ("name", "address", "phone")):
        return jsonify({"message": "Invalid input"}), 400

    new_puskesmas = Puskesmas(
        name=data["name"], address=data["address"], phone=data["phone"]
    )
    db.session.add(new_puskesmas)
    db.session.commit()

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
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_all():
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
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_puskesmas_detail(id):
    puskesmas = Puskesmas.query.get(id)
    if not puskesmas:
        return jsonify({"error": "Puskesmas tidak ditemukan"}), 404

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
@has_access(['super_admin', 'admin_puskesmas'])
def update(id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid input"}), 400

    puskesmas = Puskesmas.query.get(id)
    if not puskesmas:
        return jsonify({"message": "Puskesmas not found"}), 404

    if "name" in data:
        puskesmas.name = data["name"]
    if "address" in data:
        puskesmas.address = data["address"]
    if "phone" in data:
        puskesmas.phone = data["phone"]

    db.session.commit()

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
@has_access(['super_admin', 'admin_puskesmas'])
def delete(id):
    puskesmas = Puskesmas.query.get(id)
    if not puskesmas:
        return jsonify({"message": "Puskesmas not found"}), 404

    db.session.delete(puskesmas)
    db.session.commit()
    return jsonify({"message": "Puskesmas deleted successfully"}), 200
