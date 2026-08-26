from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import engine, SessionLocal, Base
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

# --- Pydantic schemas (API input/output shape) ---
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskResponse(TaskCreate):
    id: int
    class Config:
        from_attributes = True

# --- Dependency: DB session per request ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints ---
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Welcome to TaskFlow"}

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.TaskDB).all()

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = models.TaskDB(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated.title
    task.description = updated.description
    task.completed = updated.completed
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}