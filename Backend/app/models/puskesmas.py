from sqlalchemy import Column, Integer, String, DateTime
from .. import db
from sqlalchemy.sql import func


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
