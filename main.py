from fastapi import FastAPI

from database.database import Base, engine, SessionLocal
from repositories.user_repository import UserRepository
from routers.auth_router import auth_router
from routers.tasks_router import tasks_router
from routers.admin_router import admin_router

app = FastAPI(title="Task Tracker API", version="1.0.0")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        repo = UserRepository(db)
        if not repo.get_by_username("admin"):
            repo.create(
                email="admin@example.com",
                username="admin",
                phone="+7-900-000-00-00",
                password="Admin123",
                role="admin"
            )
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Task Tracker API is running"}


app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(admin_router)
