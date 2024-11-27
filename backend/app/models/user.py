from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import validates
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db


class User(db.Model):
    __tablename__ = "users"  # Nama tabel di database

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID pengguna, sebagai primary key dan auto-increment
    full_name = Column(String(100), nullable=False)  # Nama lengkap pengguna
    email = Column(String(100), nullable=False, unique=True)  # Email pengguna, harus unik
    password = Column(String(255), nullable=False)  # Kata sandi pengguna
    role = Column(
        Enum("super_admin", "admin_puskesmas", "admin_posyandu", "user"),  # Peran pengguna
        nullable=False,
        default="parents",  # Peran default jika tidak ditentukan
    )
    created_at = Column(DateTime, default=func.current_timestamp())  # Waktu pembuatan catatan
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()  # Waktu pembaruan catatan
    )
    reset_token = Column(String(100), nullable=True)  # Token reset kata sandi
    reset_token_expiry = Column(DateTime, nullable=True)  # Waktu kedaluwarsa token reset

    @validates("email")
    def validate_email(self, key, address):
        # Validasi untuk memastikan email mengandung '@'
        assert "@" in address
        return address

    def set_password(self, password):
        # Mengatur kata sandi dengan hash
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # Memeriksa apakah kata sandi yang diberikan cocok dengan hash
        return check_password_hash(self.password, password)


# Operasi CRUD menggunakan SQLAlchemy ORM


def createUser(full_name, email, password, role="parents"):
    # Fungsi untuk membuat pengguna baru
    new_user = User(full_name=full_name, email=email, role=role)  # Membuat objek User baru
    new_user.set_password(password)  # Mengatur kata sandi untuk pengguna
    db.session.add(new_user)  # Menambahkan objek User ke sesi
    db.session.commit()  # Menyimpan perubahan ke database
    return new_user  # Mengembalikan objek User yang baru dibuat


def updateUser(id, data):
    # Fungsi untuk memperbarui data pengguna berdasarkan ID
    user = User.query.get(id)  # Mencari pengguna berdasarkan ID
    if user:  # Memeriksa apakah pengguna ditemukan
        for key, value in data.items():  # Memperbarui atribut pengguna dengan data baru
            if key == "password":
                user.set_password(value)  # Mengatur kata sandi jika ada
            else:
                setattr(user, key, value)  # Memperbarui atribut lainnya
        db.session.commit()  # Menyimpan perubahan ke database
    return user  # Mengembalikan objek User yang diperbarui


def deleteUser(id):
    # Fungsi untuk menghapus pengguna berdasarkan ID
    user = User.query.get(id)  # Mencari pengguna berdasarkan ID
    if user:  # Memeriksa apakah pengguna ditemukan
        db.session.delete(user)  # Menghapus pengguna dari sesi
        db.session.commit()  # Menyimpan perubahan ke database
    return user is not None  # Mengembalikan True jika pengguna berhasil dihapus, False jika tidak ditemukan


def authenticate(email, password):
    # Fungsi untuk mengautentikasi pengguna berdasarkan email dan kata sandi
    user = User.query.filter_by(email=email).first()  # Mencari pengguna berdasarkan email
    if user and user.check_password(password):  # Memeriksa apakah pengguna ditemukan dan kata sandi cocok
        return {"id": user.id, "email": user.email, "role": user.role}  # Mengembalikan informasi pengguna
    return None  # Mengembalikan None jika autentikasi gagal


def getRole(user_id):
    # Fungsi untuk mendapatkan peran pengguna berdasarkan ID
    user = User.query.get(user_id)  # Mencari pengguna berdasarkan ID
    return user.role if user else None  # Mengembalikan peran pengguna jika ditemukan, None jika tidak
