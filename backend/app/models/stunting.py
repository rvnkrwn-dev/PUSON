from sqlalchemy import Column, Integer, Date, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .. import db


class Stunting(db.Model):
    __tablename__ = "stunting"

    id = Column(Integer, primary_key=True, autoincrement=True)
    anak_id = Column(Integer, ForeignKey("anak.id"), nullable=False)
    date = Column(Date, nullable=False)
    height = Column(DECIMAL(5, 2), nullable=False)
    weight = Column(DECIMAL(5, 2), nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )

    anak = relationship("Anak")


def add_stunting_data(anak_id, date, height, weight):
    new_record = Stunting(
        anak_id=anak_id,
        date=date,
        height=height,
        weight=weight,
    )
    db.session.add(new_record)
    db.session.commit()
    return new_record


def update_stunting_data(id, data):
    stunting_record = db.session.query(Stunting).get(id)
    if not stunting_record:
        return None

    if "anak_id" in data:
        stunting_record.anak_id = data["anak_id"]
    if "date" in data:
        stunting_record.date = data["date"]
    if "height" in data:
        stunting_record.height = data["height"]
    if "weight" in data:
        stunting_record.weight = data["weight"]

    db.session.commit()
    return stunting_record


def delete_stunting_data(id):
    stunting_record = db.session.query(Stunting).get(id)
    if not stunting_record:
        return False

    db.session.delete(stunting_record)
    db.session.commit()
    return True


def get_anak_data(anak_id):
    return db.session.query(Stunting).filter_by(anak_id=anak_id).all()
