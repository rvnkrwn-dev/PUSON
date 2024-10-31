from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .. import db
from sqlalchemy.sql import func
import logging


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


def generate_token(session, user_id, token, expires_at):
    new_token = RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
    session.add(new_token)
    session.commit()
    return new_token


def validate_token(session, token):
    return session.query(RefreshToken).filter_by(token=token).first()


def delete_token(session, token_id):
    token = session.query(RefreshToken).filter_by(id=token_id).first()
    if token:
        session.delete(token)
        session.commit()
    return token


def get_user(refresh_token):
    return refresh_token.user
