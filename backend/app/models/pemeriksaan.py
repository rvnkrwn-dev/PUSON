from sqlalchemy import Column, Integer, Date, Text, DateTime, ForeignKey, text
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


def addPemeriksaan(anak_id, date, result):
    sql = text("""
        INSERT INTO pemeriksaan (anak_id, date, result)
        VALUES (:anak_id, :date, :result)
        RETURNING id, anak_id, date, result, created_at, updated_at;
    """)
    result = db.session.execute(
        sql, {"anak_id": anak_id, "date": date, "result": result}
    )
    db.session.commit()
    return result.fetchone()


def updatePemeriksaan(id, data):
    sql = text("""
        UPDATE pemeriksaan
        SET anak_id = COALESCE(:anak_id, anak_id),
            date = COALESCE(:date, date),
            result = COALESCE(:result, result),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :id
        RETURNING id, anak_id, date, result, created_at, updated_at;
    """)
    result = db.session.execute(
        sql,
        {
            "id": id,
            "anak_id": data.get("anak_id"),
            "date": data.get("date"),
            "result": data.get("result"),
        },
    )
    db.session.commit()
    return result.fetchone()


def deletePemeriksaan(id):
    sql = text("""
        DELETE FROM pemeriksaan
        WHERE id = :id
        RETURNING id;
    """)
    result = db.session.execute(sql, {"id": id})
    db.session.commit()
    return result.fetchone() is not None


def getAnakData(anak_id):
    sql = text("""
        SELECT * FROM pemeriksaan
        WHERE anak_id = :anak_id;
    """)
    result = db.session.execute(sql, {"anak_id": anak_id})
    return result.fetchall()
