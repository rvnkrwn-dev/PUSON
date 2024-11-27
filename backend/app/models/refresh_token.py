from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .. import db
from sqlalchemy.sql import func
from datetime import datetime


class RefreshToken(db.Model):
    __tablename__ = "refresh_token"  # Nama tabel di database

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID refresh token, sebagai primary key dan auto-increment
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ID pengguna yang memiliki token, mengacu pada tabel users
    token = Column(String(255), nullable=False, unique=True)  # Token refresh, harus unik
    expires_at = Column(DateTime, nullable=False)  # Waktu kedaluwarsa token
    created_at = Column(DateTime, default=func.current_timestamp())  # Waktu pembuatan token
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()  # Waktu pembaruan token
    )
    user = relationship("User")  # Relasi dengan model User untuk mendapatkan informasi pengguna


def generate_token(session, user_id, token, expires_at):
    # Fungsi untuk menghasilkan token refresh baru
    new_token = RefreshToken(user_id=user_id, token=token, expires_at=expires_at)  # Membuat objek RefreshToken baru
    session.add(new_token)  # Menambahkan objek RefreshToken ke sesi
    session.commit()  # Menyimpan perubahan ke database
    return new_token  # Mengembalikan objek RefreshToken yang baru dibuat


def validate_token(session, token):
    # Fungsi untuk memvalidasi token refresh
    return session.query(RefreshToken).filter_by(token=token).first()  # Mengembalikan token jika valid, None jika tidak


def delete_token(session, token_id):
    # Fungsi untuk menghapus token refresh berdasarkan ID
    token = session.query(RefreshToken).filter_by(id=token_id).first()  # Mencari token berdasarkan ID
    if token:  # Memeriksa apakah token ditemukan
        session.delete(token)  # Menghapus token dari sesi
        session.commit()  # Menyimpan perubahan ke database
    return token  # Mengembalikan token yang dihapus (atau None jika tidak ditemukan)


def get_user(refresh_token):
    # Fungsi untuk mendapatkan pengguna yang terkait dengan token refresh
    return refresh_token.user  # Mengembalikan objek User yang terkait dengan token


def delete_refresh_token(session, user_id):
    # Menghapus semua refresh token yang terkait dengan user_id
    session.query(RefreshToken).filter_by(user_id=user_id).delete()  # Menghapus semua token yang terkait dengan pengguna
    session.commit()  # Menyimpan perubahan ke database


def delete_expired_refresh_tokens(session): 
    now = datetime.utcnow()  # Mendapatkan waktu saat ini dalam UTC
    # Hapus token refresh yang sudah kedaluwarsa 
    session.query(RefreshToken).filter(RefreshToken.expires_at < now).delete()  # Menghapus semua token yang waktu kedaluwarsanya lebih kecil dari waktu sekarang
    session.commit()  # Menyimpan perubahan ke database