from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from ..models.user import User

def is_login(f):
    # Dekorator untuk memeriksa apakah pengguna sudah login
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()  # Verifikasi JWT

            jwt_data = get_jwt()  # Ambil data dari JWT
            user_id = jwt_data.get("sub")  # Ambil ID pengguna dari payload JWT

            if not isinstance(user_id, str):
                return jsonify({"message": "Subject must be a string"}), 400  # Validasi ID pengguna

            user = User.query.get(user_id)  # Ambil pengguna dari database
            if not user:
                return jsonify({"message": "Token is invalid"}), 401  # Token tidak valid

            request.user = user  # Simpan pengguna dalam objek request
            return f(*args, **kwargs)  # Panggil fungsi yang didekorasi

        except Exception as e:
            return jsonify({"message": "Unauthorized", "statusCode": 401}), 401  # Tangani kesalahan

    return decorated_function
