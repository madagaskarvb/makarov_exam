from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db, get_current_admin
from models.user_model import User
from repositories.user_repository import UserRepository
from schemas.user_schema import UserOut

admin_router = APIRouter(prefix="/admin", tags=["Admin"])


@admin_router.get("/users", response_model=List[UserOut])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    return UserRepository(db).list_all()
