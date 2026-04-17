from pydantic import BaseModel, ConfigDict, field_validator

from typing import Optional

from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if len(value.strip()) < 3:
            raise ValueError("Название задачи должно содержать минимум 3 символа")
        return value.strip()


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        allowed = {"new", "in_progress", "done"}
        if value not in allowed:
            raise ValueError(f"Статус должен быть одним из: {allowed}")
        return value


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)