from sqlalchemy import Column, Integer, String, Enum, DateTime, text
from .. import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
import logging


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(
        Enum("super_admin", "admin_puskesmas", "admin_posyandu", "parents"),
        nullable=False,
        default="parents",
    )
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )
    reset_token = Column(String(100), nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)


def createUser(full_name, email, password, role="parents"):
    hashed_password = generate_password_hash(password)
    sql = text(""" 
        INSERT INTO users (full_name, email, password, role)
        VALUES (:full_name, :email, :password, :role);
    """)

    db.session.execute(
        sql,
        {
            "full_name": full_name,
            "email": email,
            "password": hashed_password,
            "role": role,
        },
    )

    db.session.commit()

    return db.session.execute(
        text(
            "SELECT id, full_name, email, role, created_at, updated_at FROM users WHERE email = :email"
        ),
        {"email": email},
    ).fetchone()


def updateUser(id, data):
    sql = text("""
        UPDATE users
        SET full_name = COALESCE(:full_name, full_name),
            email = COALESCE(:email, email),
            password = COALESCE(:password, password),
            role = COALESCE(:role, role),
            reset_token = COALESCE(:reset_token, reset_token),
            reset_token_expiry = COALESCE(:reset_token_expiry, reset_token_expiry),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :id
    """)

    if "password" in data and data["password"] is not None:
        data["password"] = generate_password_hash(data["password"])

    db.session.execute(
        sql,
        {
            "id": id,
            "full_name": data.get("full_name"),
            "email": data.get("email"),
            "password": data.get("password"),
            "role": data.get("role"),
            "reset_token": data.get("reset_token"),
            "reset_token_expiry": data.get("reset_token_expiry"),
        },
    )
    db.session.commit()

    return {"id": id, **data}


def deleteUser(id):
    sql = text("""
        DELETE FROM users
        WHERE id = :id
        RETURNING id;
    """)
    result = db.session.execute(sql, {"id": id})
    db.session.commit()
    return result.fetchone() is not None


def authenticate(email, password):
    user = db.session.execute(
        text(
            "SELECT id, full_name, email, password, role FROM users WHERE email = :email"
        ),
        {"email": email},
    ).fetchone()

    if user and check_password_hash(user.password, password):
        return {"id": user.id, "email": user.email, "role": user.role}
    return None


def getRole(user_id):
    sql = text("""
        SELECT role FROM users
        WHERE id = :user_id;
    """)
    result = db.session.execute(sql, {"user_id": user_id}).fetchone()
    return result.role if result else None
