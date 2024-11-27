from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from ..models.user import User

# Hierarki akses berdasarkan peran
access_hierarchy = {
    "super_admin": ["super_admin", "admin_puskesmas", "admin_posyandu", "user"],
    "admin_puskesmas": ["admin_posyandu", "user"],
    "admin_posyandu": ["admin_posyandu", "user"],
    "user": ["user"],
}

def is_role_allowed(user_role, required_roles):
    # Memeriksa apakah peran pengguna diizinkan
    if user_role in required_roles:
        return True
    for role in required_roles:
        if user_role in access_hierarchy and role in access_hierarchy[user_role]:
            return True
    return False

def has_access(required_roles):
    # Dekorator untuk memeriksa akses
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()  # Verifikasi JWT
            except Exception as e:
                return jsonify({"message": str(e)}), 401

            user_id = get_jwt_identity()  # Ambil ID pengguna dari token
            if not user_id:
                return jsonify({"message": "User identity not found in token"}), 403

            user = User.query.get(user_id)  # Ambil pengguna dari database
            if not user:
                return jsonify({"message": "User not found"}), 404

            if is_role_allowed(user.role, required_roles):
                return f(*args, **kwargs)  # Akses diizinkan

            return jsonify({"message": "Access denied"}), 403  # Akses ditolak

        return decorated_function

    return decorator
