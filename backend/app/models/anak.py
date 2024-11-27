from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .. import db


class Anak(db.Model):
    __tablename__ = "anak"  # Nama tabel di database

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID anak, primary key
    name = Column(String(100), nullable=False)  # Nama anak
    age = Column(Integer, nullable=False)  # Usia anak
    gender = Column(Enum("male", "female"), nullable=False)  # Jenis kelamin anak
    posyandu_id = Column(Integer, ForeignKey("posyandu.id"), nullable=True)  # ID posyandu yang terkait
    created_at = Column(DateTime, default=func.current_timestamp())  # Waktu pembuatan catatan
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()  # Waktu pembaruan catatan
    )

    posyandu = relationship("Posyandu")  # Relasi dengan model Posyandu


def register_anak(name, age, gender, posyandu_id):
    # Fungsi untuk mendaftarkan anak baru
    anak = Anak(name=name, age=age, gender=gender, posyandu_id=posyandu_id)  # Membuat objek Anak
    db.session.add(anak)  # Menambahkan objek Anak ke sesi
    db.session.commit()  # Menyimpan perubahan ke database
    return anak  # Mengembalikan objek Anak yang baru dibuat


def update_anak(id, data):
    # Fungsi untuk memperbarui data anak berdasarkan ID
    anak = db.session.query(Anak).get(id)  # Mencari anak berdasarkan ID
    if not anak:
        return None  # Mengembalikan None jika anak tidak ditemukan

    # Memperbarui atribut anak dengan data baru jika ada
    if "name" in data:
        anak.name = data["name"]
    if "age" in data:
        anak.age = data["age"]
    if "gender" in data:
        anak.gender = data["gender"]
    if "posyandu_id" in data:
        anak.posyandu_id = data["posyandu_id"]

    db.session.commit()  # Menyimpan perubahan ke database
    return anak  # Mengembalikan objek Anak yang diperbarui


def delete_anak(id):
    # Fungsi untuk menghapus anak berdasarkan ID
    anak = db.session.query(Anak).get(id)  # Mencari anak berdasarkan ID
    if not anak:
        return False  # Mengembalikan False jika anak tidak ditemukan

    db.session.delete(anak)  # Menghapus anak dari sesi
    db.session.commit()  # Menyimpan perubahan ke database
    return True  # Mengembalikan True jika penghapusan berhasil
