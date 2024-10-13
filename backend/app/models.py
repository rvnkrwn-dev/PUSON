from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum,
    DateTime,
    Text,
    DECIMAL,
    Date,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import db


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(
        Enum("super_admin", "admin_puskesmas", "admin_posyandu", "user"), nullable=False
    )
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )
    reset_token = Column(String(100), nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)


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


class RefreshToken(db.Model):
    __tablename__ = "refresh_token"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )
    user = relationship("User")


class Log(db.Model):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.current_timestamp())
    user = relationship("User")
