from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .. import db
from sqlalchemy.sql import func


class Anak(db.Model):
    __tablename__ = "anak"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum("male", "female"), nullable=False)
    posyandu_id = Column(Integer, ForeignKey("posyandu.id"), nullable=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )
    posyandu = relationship("Posyandu")
