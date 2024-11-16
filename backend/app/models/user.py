from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import validates
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(
        Enum("super_admin", "admin_puskesmas", "admin_posyandu", "user"),
        nullable=False,
        default="parents",
    )
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )
    reset_token = Column(String(100), nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)

    @validates("email")
    def validate_email(self, key, address):
        assert "@" in address
        return address

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Operasi CRUD menggunakan SQLAlchemy ORM


def createUser(full_name, email, password, role="parents"):
    new_user = User(full_name=full_name, email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def updateUser(id, data):
    user = User.query.get(id)
    if user:
        for key, value in data.items():
            if key == "password":
                user.set_password(value)
            else:
                setattr(user, key, value)
        db.session.commit()
    return user


def deleteUser(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return user is not None


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return {"id": user.id, "email": user.email, "role": user.role}
    return None


def getRole(user_id):
    user = User.query.get(user_id)
    return user.role if user else None
