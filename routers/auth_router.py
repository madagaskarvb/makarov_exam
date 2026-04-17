from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from dependencies import get_db, get_current_user
from models.user_model import User
from schemas.user_schema import LoginResponse, RegisterRequest, UserOut
from security.security import create_access_token
from services.auth_service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", response_model=UserOut, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return AuthService(db).register_user(data)


@auth_router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = AuthService(db).authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role,
        "username": user.username
    })

    return {"access_token": token, "token_type": "bearer"}


@auth_router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
