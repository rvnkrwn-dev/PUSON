from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .. import db


class Posyandu(db.Model):
    __tablename__ = "posyandu"  # Nama tabel di database

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID posyandu, sebagai primary key dan auto-increment
    puskesmas_id = Column(Integer, ForeignKey("puskesmas.id"), nullable=False)  # ID puskesmas yang terkait, mengacu pada tabel puskesmas
    name = Column(String(100), nullable=False)  # Nama posyandu
    address = Column(String(255), nullable=False)  # Alamat posyandu
    phone = Column(String(20), nullable=False)  # Nomor telepon posyandu
    created_at = Column(DateTime, default=func.current_timestamp())  # Waktu pembuatan catatan
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()  # Waktu pembaruan catatan
    )

    puskesmas = relationship("Puskesmas")  # Relasi dengan model Puskesmas untuk mendapatkan informasi puskesmas


def createPosyandu(puskesmas_id, name, address, phone):
    # Fungsi untuk membuat posyandu baru
    new_posyandu = Posyandu(
        puskesmas_id=puskesmas_id, name=name, address=address, phone=phone  # Membuat objek Posyandu baru
    )
    db.session.add(new_posyandu)  # Menambahkan objek Posyandu ke sesi
    db.session.commit()  # Menyimpan perubahan ke database
    return new_posyandu  # Mengembalikan objek Posyandu yang baru dibuat


def updatePosyandu(id, data):
    # Fungsi untuk memperbarui data posyandu berdasarkan ID
    posyandu = Posyandu.query.get(id)  # Mencari posyandu berdasarkan ID
    if posyandu:  # Memeriksa apakah posyandu ditemukan
        for key, value in data.items():  # Memperbarui atribut posyandu dengan data baru
            setattr(posyandu, key, value)
        db.session.commit()  # Menyimpan perubahan ke database
    return posyandu  # Mengembalikan objek Posyandu yang diperbarui


def deletePosyandu(id):
    # Fungsi untuk menghapus posyandu berdasarkan ID
    posyandu = Posyandu.query.get(id)  # Mencari posyandu berdasarkan ID
    if posyandu:  # Memeriksa apakah posyandu ditemukan
        db.session.delete(posyandu)  # Menghapus posyandu dari sesi
        db.session.commit()  # Menyimpan perubahan ke database
    return posyandu is not None  # Mengembalikan True jika posyandu berhasil dihapus, False jika tidak ditemukan


def getAnakList():
    # Fungsi untuk mendapatkan semua posyandu dari database
    return Posyandu.query.all()  # Mengembalikan semua catatan posyandu
