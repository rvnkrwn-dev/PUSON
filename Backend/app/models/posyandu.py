from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .. import db
from sqlalchemy.sql import func


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
