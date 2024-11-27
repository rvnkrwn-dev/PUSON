from sqlalchemy import Column, Integer, Date, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .. import db


class Stunting(db.Model):
    __tablename__ = "stunting"  # Nama tabel di database

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID stunting, sebagai primary key dan auto-increment
    anak_id = Column(Integer, ForeignKey("anak.id"), nullable=False)  # ID anak yang terkait, mengacu pada tabel anak
    date = Column(Date, nullable=False)  # Tanggal pengukuran stunting
    height = Column(DECIMAL(5, 2), nullable=False)  # Tinggi anak dalam format desimal (maksimal 5 digit, 2 desimal)
    weight = Column(DECIMAL(5, 2), nullable=False)  # Berat anak dalam format desimal (maksimal 5 digit, 2 desimal)
    created_at = Column(DateTime, default=func.current_timestamp())  # Waktu pembuatan catatan
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()  # Waktu pembaruan catatan
    )

    anak = relationship("Anak")  # Relasi dengan model Anak untuk mendapatkan informasi anak


def add_stunting_data(anak_id, date, height, weight):
    # Fungsi untuk menambahkan data stunting baru
    new_record = Stunting(
        anak_id=anak_id,  # ID anak yang terkait
        date=date,  # Tanggal pengukuran
        height=height,  # Tinggi anak
        weight=weight,  # Berat anak
    )
    db.session.add(new_record)  # Menambahkan objek Stunting ke sesi
    db.session.commit()  # Menyimpan perubahan ke database
    return new_record  # Mengembalikan objek Stunting yang baru dibuat


def update_stunting_data(id, data):
    # Fungsi untuk memperbarui data stunting berdasarkan ID
    stunting_record = db.session.query(Stunting).get(id)  # Mencari catatan stunting berdasarkan ID
    if not stunting_record:
        return None  # Mengembalikan None jika catatan tidak ditemukan

    # Memperbarui atribut stunting dengan data baru jika ada
    if "anak_id" in data:
        stunting_record.anak_id = data["anak_id"]
    if "date" in data:
        stunting_record.date = data["date"]
    if "height" in data:
        stunting_record.height = data["height"]
    if "weight" in data:
        stunting_record.weight = data["weight"]

    db.session.commit()  # Menyimpan perubahan ke database
    return stunting_record  # Mengembalikan objek Stunting yang diperbarui
