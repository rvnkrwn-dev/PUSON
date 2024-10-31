from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, text
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


def createPosyandu(puskesmas_id, name, address, phone):
    sql = text("""
        INSERT INTO posyandu (puskesmas_id, name, address, phone)
        VALUES (:puskesmas_id, :name, :address, :phone)
        RETURNING id, puskesmas_id, name, address, phone, created_at, updated_at;
    """)
    result = db.session.execute(
        sql,
        {
            "puskesmas_id": puskesmas_id,
            "name": name,
            "address": address,
            "phone": phone,
        },
    )
    db.session.commit()
    return result.fetchone()


def updatePosyandu(id, data):
    sql = text("""
        UPDATE posyandu
        SET puskesmas_id = COALESCE(:puskesmas_id, puskesmas_id),
            name = COALESCE(:name, name),
            address = COALESCE(:address, address),
            phone = COALESCE(:phone, phone),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :id
        RETURNING id, puskesmas_id, name, address, phone, created_at, updated_at;
    """)
    result = db.session.execute(
        sql,
        {
            "id": id,
            "puskesmas_id": data.get("puskesmas_id"),
            "name": data.get("name"),
            "address": data.get("address"),
            "phone": data.get("phone"),
        },
    )
    db.session.commit()
    return result.fetchone()


def deletePosyandu(id):
    sql = text("""
        DELETE FROM posyandu
        WHERE id = :id
        RETURNING id;
    """)
    result = db.session.execute(sql, {"id": id})
    db.session.commit()
    return result.fetchone() is not None


def getAnakList():
    sql = text("""
        SELECT * FROM posyandu;
    """)
    result = db.session.execute(sql)
    return result.fetchall()
