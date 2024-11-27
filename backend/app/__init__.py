import os
from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv()  # Memuat variabel lingkungan dari file .env

db = SQLAlchemy()  # Membuat instance SQLAlchemy untuk interaksi dengan database

def create_app():
    # Fungsi untuk membuat dan mengkonfigurasi aplikasi Flask
    app = Flask(__name__)  # Membuat instance Flask

    # Mengatur URI database menggunakan variabel lingkungan
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('DATABASE_USER')}:"  # Mengambil username database
        f"{os.getenv('DATABASE_PASSWORD')}@"  # Mengambil password database
        f"{os.getenv('DATABASE_HOST')}/"  # Mengambil host database
        f"{os.getenv('DATABASE_NAME')}"  # Mengambil nama database
    )
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Menonaktifkan pelacakan modifikasi objek untuk efisiensi

    db.init_app(app)  # Menginisialisasi SQLAlchemy dengan aplikasi Flask

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")  # Mengambil kunci rahasia dari variabel lingkungan
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "UIAHs87uagsd")  # Mengambil kunci rahasia JWT

    # Mengatur nama cookie untuk akses dan refresh token
    app.config["JWT_ACCESS_COOKIE_NAME"] = "987AUgh8712gui"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "*&As6yuaiGS"

    app.config["JWT_BLACKLIST_ENABLED"] = True  # Mengaktifkan blacklist untuk token
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]  # Menentukan jenis token yang akan diperiksa blacklist

    jwt = JWTManager(app)  # Menginisialisasi JWTManager dengan aplikasi Flask
    
    with app.app_context():  # Membuat konteks aplikasi untuk menjalankan kode di dalamnya
        db.create_all()  # Membuat semua tabel di database yang didefinisikan oleh model
        from .controllers import init_auth_blueprints  # Mengimpor fungsi untuk menginisialisasi blueprint

        init_auth_blueprints(app)  # Menginisialisasi blueprint untuk otentikasi

    return app  # Mengembalikan instance aplikasi Flask
