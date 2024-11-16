from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .. import db


class Posyandu(db.Model):
    __tablename__ = "posyandu"

    id = Column(Integer, primary_key=True, autoincrement=True)
    puskesmas_id = Column(Integer, ForeignKey("puskesmas.id"), nullable=False)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )

    puskesmas = relationship("Puskesmas")


# Operasi CRUD menggunakan SQLAlchemy ORM


def createPosyandu(puskesmas_id, name, address, phone):
    new_posyandu = Posyandu(
        puskesmas_id=puskesmas_id, name=name, address=address, phone=phone
    )
    db.session.add(new_posyandu)
    db.session.commit()
    return new_posyandu


def updatePosyandu(id, data):
    posyandu = Posyandu.query.get(id)
    if posyandu:
        for key, value in data.items():
            setattr(posyandu, key, value)
        db.session.commit()
    return posyandu


def deletePosyandu(id):
    posyandu = Posyandu.query.get(id)
    if posyandu:
        db.session.delete(posyandu)
        db.session.commit()
    return posyandu is not None


def getAnakList():
    return Posyandu.query.all()
