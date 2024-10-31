from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .. import db
from sqlalchemy.sql import func


class Log(db.Model):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.current_timestamp())
    user = relationship("User")


def add_log(session, user_id, action, description):
    new_log = Log(user_id=user_id, action=action, description=description)
    session.add(new_log)
    session.commit()
    return new_log


def get_user_logs(session, user_id):
    return session.query(Log).filter_by(user_id=user_id).all()


def delete_log(session, log_id):
    log = session.query(Log).filter_by(id=log_id).first()
    if log:
        session.delete(log)
        session.commit()
    return log
