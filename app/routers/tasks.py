from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# POST /tasks — create a new task (protected)
@router.post("/", response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # must be logged in
):
    new_task = models.Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# GET /tasks — get all tasks (protected)
@router.get("/", response_model=list[schemas.TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # must be logged in
):
    return db.query(models.Task).all()

# GET /tasks/{id} — get one task (protected)
@router.get("/{id}", response_model=schemas.TaskResponse)
def get_task(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # must be logged in
):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# PUT /tasks/{id} — update a task (protected)
@router.put("/{id}", response_model=schemas.TaskResponse)
def update_task(
    id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # must be logged in
):
    db_task = db.query(models.Task).filter(models.Task.id == id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.model_dump().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

# DELETE /tasks/{id} — delete a task (protected)
@router.delete("/{id}")
def delete_task(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # must be logged in
):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}