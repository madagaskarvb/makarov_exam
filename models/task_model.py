from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, create_engine, or_
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker

from datetime import datetime, timedelta, timezone

from database.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, default="")
    status = Column(String(30), default="new", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tasks")