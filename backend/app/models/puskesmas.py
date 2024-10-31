from sqlalchemy import Column, Integer, String, DateTime, text
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


def createPuskesmas(name, address, phone):
    sql = text("""
        INSERT INTO puskesmas (name, address, phone)
        VALUES (:name, :address, :phone)
        RETURNING id, name, address, phone, created_at, updated_at;
    """)
    result = db.session.execute(sql, {"name": name, "address": address, "phone": phone})
    db.session.commit()
    return result.fetchone()


def updatePuskesmas(id, data):
    sql = text("""
        UPDATE puskesmas
        SET name = COALESCE(:name, name),
            address = COALESCE(:address, address),
            phone = COALESCE(:phone, phone),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :id
        RETURNING id, name, address, phone, created_at, updated_at;
    """)
    result = db.session.execute(
        sql,
        {
            "id": id,
            "name": data.get("name"),
            "address": data.get("address"),
            "phone": data.get("phone"),
        },
    )
    db.session.commit()
    return result.fetchone()


def deletePuskesmas(id):
    sql = text("""
        DELETE FROM puskesmas
        WHERE id = :id
        RETURNING id;
    """)
    result = db.session.execute(sql, {"id": id})
    db.session.commit()
    return result.fetchone() is not None


def getPosyanduList():
    sql = text("""
        SELECT * FROM puskesmas;
    """)
    result = db.session.execute(sql)
    return result.fetchall()
