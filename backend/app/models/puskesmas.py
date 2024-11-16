from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .. import db


class Puskesmas(db.Model):
    __tablename__ = "puskesmas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )


def create_puskesmas(name, address, phone):
    new_puskesmas = Puskesmas(name=name, address=address, phone=phone)
    db.session.add(new_puskesmas)
    db.session.commit()
    return new_puskesmas


def update_puskesmas(id, data):
    puskesmas = db.session.query(Puskesmas).get(id)
    if not puskesmas:
        return None

    if "name" in data:
        puskesmas.name = data["name"]
    if "address" in data:
        puskesmas.address = data["address"]
    if "phone" in data:
        puskesmas.phone = data["phone"]

    db.session.commit()
    return puskesmas


def delete_puskesmas(id):
    puskesmas = db.session.query(Puskesmas).get(id)
    if not puskesmas:
        return False

    db.session.delete(puskesmas)
    db.session.commit()
    return True


def get_puskesmas_list():
    return db.session.query(Puskesmas).all()
