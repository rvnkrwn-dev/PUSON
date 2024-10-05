from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Role(db.Model):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    users = relationship("User", back_populates="role")


class Posyandu(db.Model):
    __tablename__ = "posyandu"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    users = relationship("User", back_populates="posyandu")


class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    _password = Column(
        "password", String(255), nullable=False
    )
    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=True)
    posyandu_id = Column(Integer, ForeignKey("posyandu.id"), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

    role = relationship("Role", back_populates="users")
    posyandu = relationship("Posyandu", back_populates="users")

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        # Generates and stores the password hash with a salt length of 10
        self._password = generate_password_hash(
            password, method="pbkdf2:sha256", salt_length=10
        )

    def check_password(self, password):
        # Checks the password against the stored hash
        return check_password_hash(self._password, password)
