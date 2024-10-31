from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, text
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
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    posyandu = relationship("Posyandu")

def registerAnak(name, age, gender, posyandu_id):
    sql = text("""
        INSERT INTO anak (name, age, gender, posyandu_id)
        VALUES (:name, :age, :gender, :posyandu_id)
        RETURNING id, name, age, gender, posyandu_id, created_at, updated_at;
    """)
    result = db.session.execute(sql, {
        'name': name,
        'age': age,
        'gender': gender,
        'posyandu_id': posyandu_id
    })
    db.session.commit()
    return result.fetchone()  # Returns the newly registered record

def updateAnak(id, data):
    sql = text("""
        UPDATE anak
        SET name = COALESCE(:name, name),
            age = COALESCE(:age, age),
            gender = COALESCE(:gender, gender),
            posyandu_id = COALESCE(:posyandu_id, posyandu_id),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :id
        RETURNING id, name, age, gender, posyandu_id, created_at, updated_at;
    """)
    result = db.session.execute(sql, {
        'id': id,
        'name': data.get('name'),
        'age': data.get('age'),
        'gender': data.get('gender'),
        'posyandu_id': data.get('posyandu_id')
    })
    db.session.commit()
    return result.fetchone()  # Returns the updated record or None if not found

def deleteAnak(id):
    sql = text("""
        DELETE FROM anak
        WHERE id = :id
        RETURNING id;
    """)
    result = db.session.execute(sql, {'id': id})
    db.session.commit()
    return result.fetchone() is not None  # Returns True if a record was deleted

def getPemeriksaanHistory(posyandu_id):
    sql = text("""
        SELECT * FROM pemeriksaan
        WHERE posyandu_id = :posyandu_id;
    """)
    result = db.session.execute(sql, {'posyandu_id': posyandu_id})
    return result.fetchall()  # Returns a list of all records related to pemeriksaan

def getStuntingHistory(anak_id):
    sql = text("""
        SELECT * FROM stunting
        WHERE anak_id = :anak_id;
    """)
    result = db.session.execute(sql, {'anak_id': anak_id})
    return result.fetchall()  # Returns a list of all records related to stunting
