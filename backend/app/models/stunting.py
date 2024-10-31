from sqlalchemy import Column, Integer, Date, DECIMAL, DateTime, ForeignKey, text
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


def addStuntingData(anak_id, date, height, weight):
    sql = text("""
        INSERT INTO stunting (anak_id, date, height, weight)
        VALUES (:anak_id, :date, :height, :weight)
        RETURNING id, anak_id, date, height, weight, created_at, updated_at;
    """)
    result = db.session.execute(
        sql, {"anak_id": anak_id, "date": date, "height": height, "weight": weight}
    )
    db.session.commit()
    return result.fetchone()


def updateStuntingData(id, data):
    sql = text("""
        UPDATE stunting
        SET anak_id = COALESCE(:anak_id, anak_id),
            date = COALESCE(:date, date),
            height = COALESCE(:height, height),
            weight = COALESCE(:weight, weight),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :id
        RETURNING id, anak_id, date, height, weight, created_at, updated_at;
    """)
    result = db.session.execute(
        sql,
        {
            "id": id,
            "anak_id": data.get("anak_id"),
            "date": data.get("date"),
            "height": data.get("height"),
            "weight": data.get("weight"),
        },
    )
    db.session.commit()
    return result.fetchone()


def deleteStuntingData(id):
    sql = text("""
        DELETE FROM stunting
        WHERE id = :id
        RETURNING id;
    """)
    result = db.session.execute(sql, {"id": id})
    db.session.commit()
    return result.fetchone() is not None


def getAnakData(anak_id):
    sql = text("""
        SELECT * FROM stunting
        WHERE anak_id = :anak_id;
    """)
    result = db.session.execute(sql, {"anak_id": anak_id})
    return result.fetchall()
