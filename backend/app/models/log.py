from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .. import db
from sqlalchemy.sql import func


class Log(db.Model):
    __tablename__ = "logs"  # Nama tabel di database

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID log, primary key
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ID pengguna yang melakukan aksi
    action = Column(String(255), nullable=False)  # Jenis aksi yang dilakukan
    description = Column(Text)  # Deskripsi dari aksi
    created_at = Column(DateTime, default=func.current_timestamp())  # Waktu pembuatan log
    user = relationship("User")  # Relasi dengan model User


def add_log(session, user_id, action, description):
    # Fungsi untuk menambahkan log baru
    new_log = Log(user_id=user_id, action=action, description=description)  # Membuat objek Log baru
    session.add(new_log)  # Menambahkan objek Log ke sesi
    session.commit()  # Menyimpan perubahan ke database
    return new_log  # Mengembalikan objek Log yang baru dibuat


def get_user_logs(session, user_id):
    # Fungsi untuk mendapatkan semua log berdasarkan ID pengguna
    return session.query(Log).filter_by(user_id=user_id).all()  # Mengembalikan semua log terkait pengguna


def delete_log(session, log_id):
    # Fungsi untuk menghapus log berdasarkan ID
    log = session.query(Log).filter_by(id=log_id).first()  # Mencari log berdasarkan ID
    if log:
        session.delete(log)  # Menghapus log dari sesi
        session.commit()  # Menyimpan perubahan ke database
    return log  # Mengembalikan log yang dihapus (atau None jika tidak ditemukan)
