from flask import Blueprint, jsonify, request
from ..models.log import Log
from ..models.user import User
from ..middlewares.is_login import is_login
from ..middlewares.has_access import has_access
from flask_jwt_extended import jwt_required

log_bp = Blueprint("log_bp", __name__)

@log_bp.route("/logs", methods=["GET"])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_logs():
    # Ambil parameter halaman dan jumlah data per halaman dari query string
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    
    # Ambil query parameter untuk filter berdasarkan user_id
    user_id = request.args.get("user_id", None, type=int)

    # Query dasar untuk log
    query = Log.query

    # Filter berdasarkan user_id jika diberikan
    if user_id:
        query = query.filter_by(user_id=user_id)

    # Pagination
    logs_paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    # Data log untuk halaman saat ini
    logs_list = [
        {
            "id": log.id,
            "user_id": log.user_id,
            "user_name": log.user.full_name if log.user else None,
            "action": log.action,
            "description": log.description,
            "created_at": log.created_at,
        }
        for log in logs_paginated.items
    ]

    # Mengembalikan respons dengan detail log yang ditemukan dan informasi pagination
    return jsonify(
        {
            "data": logs_list,
            "pagination": {
                "total": logs_paginated.total,  # Total semua data
                "pages": logs_paginated.pages,  # Total halaman
                "current_page": logs_paginated.page,  # Halaman saat ini
                "per_page": logs_paginated.per_page,  # Jumlah data per halaman
                "has_next_page": logs_paginated.has_next,  # Apakah ada halaman berikutnya
                "has_previous_page": logs_paginated.has_prev,  # Apakah ada halaman sebelumnya
                "next_page": logs_paginated.next_num if logs_paginated.has_next else None,
                "previous_page": logs_paginated.prev_num if logs_paginated.has_prev else None
            }
        }
    ), 200
