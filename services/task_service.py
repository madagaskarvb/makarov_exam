import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from cache.redis_client import redis_client
from models.task_model import Task
from models.user_model import User
from repositories.task_repository import TaskRepository
from schemas.task_schema import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.task_repo = TaskRepository(db)

    def _cache_key(self, user_id: int) -> str:
        return f"user:{user_id}:tasks"

    def _serialize_task(self, task: Task) -> dict:
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "owner_id": task.owner_id,
            "created_at": task.created_at.isoformat()
        }

    def _invalidate_tasks_cache(self, user_id: int):
        if redis_client:
            redis_client.delete(self._cache_key(user_id))

    def create_task(self, user_id: int, data: TaskCreate):
        task = self.task_repo.create(
            owner_id=user_id,
            title=data.title,
            description=data.description or ""
        )
        self._invalidate_tasks_cache(user_id)
        return task

    def list_tasks(self, user_id: int):
        cache_key = self._cache_key(user_id)

        if redis_client:
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

        tasks = self.task_repo.list_by_owner(user_id)
        result = [self._serialize_task(task) for task in tasks]

        if redis_client:
            redis_client.setex(cache_key, 60, json.dumps(result, ensure_ascii=False))

        return result

    def get_task_for_user(self, task_id: int, current_user: User):
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        if task.owner_id != current_user.id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Нет доступа к задаче")

        return task

    def update_task(self, task_id: int, data: TaskUpdate, current_user: User):
        task = self.get_task_for_user(task_id, current_user)

        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.status is not None:
            task.status = data.status

        updated_task = self.task_repo.update(task)
        self._invalidate_tasks_cache(updated_task.owner_id)
        return updated_task

    def delete_task(self, task_id: int, current_user: User):
        task = self.get_task_for_user(task_id, current_user)
        owner_id = task.owner_id
        self.task_repo.delete(task)
        self._invalidate_tasks_cache(owner_id)
