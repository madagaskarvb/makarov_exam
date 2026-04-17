from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, create_engine, or_
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker

from datetime import datetime, timedelta, timezone

from database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="owner", cascade="all, delete")