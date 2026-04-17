from models.task_model import Task

from security.security import hash_password

from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, create_engine, or_

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, owner_id: int, title: str, description: str = ""):
        task = Task(
            owner_id=owner_id,
            title=title,
            description=description,
            status="new"
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def list_by_owner(self, owner_id: int):
        return self.db.query(Task).filter(Task.owner_id == owner_id).all()

    def update(self, task: Task):
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task):
        self.db.delete(task)
        self.db.commit()