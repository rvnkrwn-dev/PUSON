from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .. import db


class Anak(db.Model):
    __tablename__ = "anak"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum("male", "female"), nullable=False)
    posyandu_id = Column(Integer, ForeignKey("posyandu.id"), nullable=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )

    posyandu = relationship("Posyandu")


def register_anak(name, age, gender, posyandu_id):
    anak = Anak(name=name, age=age, gender=gender, posyandu_id=posyandu_id)
    db.session.add(anak)
    db.session.commit()
    return anak  # Returns the newly registered `Anak` object


def update_anak(id, data):
    anak = db.session.query(Anak).get(id)
    if not anak:
        return None

    if "name" in data:
        anak.name = data["name"]
    if "age" in data:
        anak.age = data["age"]
    if "gender" in data:
        anak.gender = data["gender"]
    if "posyandu_id" in data:
        anak.posyandu_id = data["posyandu_id"]

    db.session.commit()
    return anak  # Returns the updated `Anak` object


def delete_anak(id):
    anak = db.session.query(Anak).get(id)
    if not anak:
        return False

    db.session.delete(anak)
    db.session.commit()
    return True  # Returns True if a record was deleted


def get_pemeriksaan_history(posyandu_id):
    return db.session.query(Pemeriksaan).filter_by(posyandu_id=posyandu_id).all()


def get_stunting_history(anak_id):
    return db.session.query(Stunting).filter_by(anak_id=anak_id).all()
