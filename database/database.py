from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, create_engine, or_
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()