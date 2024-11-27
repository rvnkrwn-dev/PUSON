from sqlalchemy import Column, Integer, Date, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .. import db
from ..services.check_stunting import check_stunting


class Pemeriksaan(db.Model):
    __tablename__ = "pemeriksaan"  # Nama tabel di database

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID pemeriksaan, sebagai primary key dan auto-increment
    anak_id = Column(Integer, ForeignKey("anak.id"), nullable=False)  # ID anak yang terkait, mengacu pada tabel anak
    date = Column(Date, nullable=False)  # Tanggal pemeriksaan
    result = Column(Text, nullable=False)  # Hasil pemeriksaan
    created_at = Column(DateTime, default=func.current_timestamp())  # Waktu pembuatan catatan
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()  # Waktu pembaruan catatan
    )

    anak = relationship("Anak")  # Relasi dengan model Anak untuk mendapatkan informasi anak


def add_pemeriksaan(anak_id, date, result=None):
    # Fungsi untuk menambahkan pemeriksaan baru
    result = check_stunting(anak_id) if result is None else result  # Memeriksa status stunting jika hasil tidak diberikan

    # Membuat objek Pemeriksaan baru
    pemeriksaan = Pemeriksaan(anak_id=anak_id, date=date, result=result)

    db.session.add(pemeriksaan)  # Menambahkan objek Pemeriksaan ke sesi
    db.session.commit()  # Menyimpan perubahan ke database

    return pemeriksaan  # Mengembalikan objek Pemeriksaan yang baru dibuat


def update_pemeriksaan(id, data):
    # Fungsi untuk memperbarui data pemeriksaan berdasarkan ID
    pemeriksaan = db.session.query(Pemeriksaan).get(id)  # Mencari pemeriksaan berdasarkan ID
    if not pemeriksaan:
        return None  # Mengembalikan None jika pemeriksaan tidak ditemukan

    # Memperbarui atribut pemeriksaan dengan data baru jika ada
    if "anak_id" in data:
        pemeriksaan.anak_id = data["anak_id"]
    if "date" in data:
        pemeriksaan.date = data["date"]
    if "result" in data:
        pemeriksaan.result = data["result"]

    db.session.commit()  # Menyimpan perubahan ke database

    # Jika hasil tidak diberikan dalam data, perbarui hasil berdasarkan status stunting
    if "result" not in data:
        pemeriksaan.result = check_stunting(pemeriksaan.anak_id)
        db.session.commit()  # Menyimpan perubahan ke database

    return pemeriksaan  # Mengembalikan objek Pemeriksaan yang diperbarui


def delete_pemeriksaan(id):
    # Fungsi untuk menghapus pemeriksaan berdasarkan ID
    pemeriksaan = db.session.query(Pemeriksaan).get(id)  # Mencari pemeriksaan berdasarkan ID
    if not pemeriksaan:
        return False  # Mengembalikan False jika pemeriksaan tidak ditemukan

    db.session.delete(pemeriksaan)  # Menghapus pemeriksaan dari sesi
    db.session.commit()  # Menyimpan perubahan ke database
    return True  # Mengembalikan True jika penghapusan berhasil


def get_anak_data(anak_id):
    # Fungsi untuk mendapatkan semua pemeriksaan berdasarkan ID anak
    return db.session.query(Pemeriksaan).filter_by(anak_id=anak_id).all()  # Mengembalikan semua pemeriksaan terkait anak

