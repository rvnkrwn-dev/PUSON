from sqlalchemy import Column, Integer, Date, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .. import db
from sqlalchemy.sql import func


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
