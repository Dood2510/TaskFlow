from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="TaskFlow API")

# --- Data model ---
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

# --- In-memory "database" ---
tasks: list[Task] = []
next_id = 1

# --- Endpoints ---
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Welcome to TaskFlow"}

@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    global next_id
    task.id = next_id
    next_id += 1
    tasks.append(task)
    return task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_task.id = task_id
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")