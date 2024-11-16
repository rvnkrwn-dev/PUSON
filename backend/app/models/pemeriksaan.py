from sqlalchemy import Column, Integer, Date, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .. import db


class Pemeriksaan(db.Model):
    __tablename__ = "pemeriksaan"

    id = Column(Integer, primary_key=True, autoincrement=True)
    anak_id = Column(Integer, ForeignKey("anak.id"), nullable=False)
    date = Column(Date, nullable=False)
    result = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )

    anak = relationship("Anak")


def add_pemeriksaan(anak_id, date, result):
    pemeriksaan = Pemeriksaan(anak_id=anak_id, date=date, result=result)
    db.session.add(pemeriksaan)
    db.session.commit()
    return pemeriksaan


def update_pemeriksaan(id, data):
    pemeriksaan = db.session.query(Pemeriksaan).get(id)
    if not pemeriksaan:
        return None

    if "anak_id" in data:
        pemeriksaan.anak_id = data["anak_id"]
    if "date" in data:
        pemeriksaan.date = data["date"]
    if "result" in data:
        pemeriksaan.result = data["result"]

    db.session.commit()
    return pemeriksaan


def delete_pemeriksaan(id):
    pemeriksaan = db.session.query(Pemeriksaan).get(id)
    if not pemeriksaan:
        return False

    db.session.delete(pemeriksaan)
    db.session.commit()
    return True


def get_anak_data(anak_id):
    return db.session.query(Pemeriksaan).filter_by(anak_id=anak_id).all()
