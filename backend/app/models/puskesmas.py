from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .. import db


class Puskesmas(db.Model):
    __tablename__ = "puskesmas"  # Nama tabel di database

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID puskesmas, sebagai primary key dan auto-increment
    name = Column(String(100), nullable=False)  # Nama puskesmas
    address = Column(String(255), nullable=False)  # Alamat puskesmas
    phone = Column(String(20), nullable=False)  # Nomor telepon puskesmas
    created_at = Column(DateTime, default=func.current_timestamp())  # Waktu pembuatan catatan
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()  # Waktu pembaruan catatan
    )


def create_puskesmas(name, address, phone):
    # Fungsi untuk membuat puskesmas baru
    new_puskesmas = Puskesmas(name=name, address=address, phone=phone)  # Membuat objek Puskesmas baru
    db.session.add(new_puskesmas)  # Menambahkan objek Puskesmas ke sesi
    db.session.commit()  # Menyimpan perubahan ke database
    return new_puskesmas  # Mengembalikan objek Puskesmas yang baru dibuat


def update_puskesmas(id, data):
    # Fungsi untuk memperbarui data puskesmas berdasarkan ID
    puskesmas = db.session.query(Puskesmas).get(id)  # Mencari puskesmas berdasarkan ID
    if not puskesmas:
        return None  # Mengembalikan None jika puskesmas tidak ditemukan

    # Memperbarui atribut puskesmas dengan data baru jika ada
    if "name" in data:
        puskesmas.name = data["name"]
    if "address" in data:
        puskesmas.address = data["address"]
    if "phone" in data:
        puskesmas.phone = data["phone"]

    db.session.commit()  # Menyimpan perubahan ke database
    return puskesmas  # Mengembalikan objek Puskesmas yang diperbarui


def delete_puskesmas(id):
    # Fungsi untuk menghapus puskesmas berdasarkan ID
    puskesmas = db.session.query(Puskesmas).get(id)  # Mencari puskesmas berdasarkan ID
    if not puskesmas:
        return False  # Mengembalikan False jika puskesmas tidak ditemukan

    db.session.delete(puskesmas)  # Menghapus puskesmas dari sesi
    db.session.commit()  # Menyimpan perubahan ke database
    return True  # Mengembalikan True jika penghapusan berhasil


def get_puskesmas_list():
    # Fungsi untuk mendapatkan semua puskesmas dari database
    return db.session.query(Puskesmas).all()  # Mengembalikan semua catatan puskesmas
