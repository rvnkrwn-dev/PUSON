from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Puskesmas(db.Model):
    __tablename__ = 'puskesmas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Posyandu(db.Model):
    __tablename__ = 'posyandu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    puskesmas_id = Column(Integer, ForeignKey('puskesmas.id', ondelete='CASCADE'))
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    puskesmas = relationship("Puskesmas")

class Role(db.Model):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('role.id', ondelete='SET NULL'))
    posyandu_id = Column(Integer, ForeignKey('posyandu.id', ondelete='SET NULL'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    reset_token = Column(String(255))
    reset_token_expiry = Column(DateTime)
    role = relationship("Role")
    posyandu = relationship("Posyandu")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Child(db.Model):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(Enum('male', 'female'), nullable=False)
    weight = Column(Float)
    height = Column(Float)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user = relationship("User")

class DataCheckup(db.Model):
    __tablename__ = 'data_checkup'
    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey('child.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    checkup_date = Column(DateTime, nullable=False)
    weight = Column(Float)
    height = Column(Float)
    head_circumference = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    child = relationship("Child")
    user = relationship("User")

class Stunting(db.Model):
    __tablename__ = 'stunting'
    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey('child.id', ondelete='CASCADE'))
    stunting_status = Column(Enum('normal', 'stunted'), nullable=False)
    date_assessed = Column(DateTime, nullable=False)
    assessment_notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    child = relationship("Child")

class RefreshTokens(db.Model):
    __tablename__ = 'refresh_tokens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    token = Column(String(255), nullable=False)
    user = relationship("User")
