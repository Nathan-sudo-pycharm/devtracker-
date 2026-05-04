from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

# APIRouter groups related endpoints together
# prefix="/tasks" means all routes here start with /tasks
# tags=["Tasks"] groups them in Swagger UI
router = APIRouter(prefix="/tasks", tags=["Tasks"])

# POST /tasks — create a new task
# response_model tells FastAPI what shape to return
@router.post("/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    # Convert Pydantic schema to a SQLAlchemy model object
    new_task = models.Task(**task.model_dump())
    db.add(new_task)      # stage the new task
    db.commit()           # save to database
    db.refresh(new_task)  # reload from DB to get generated fields (id, created_at)
    return new_task

# GET /tasks — return all tasks
@router.get("/", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

# GET /tasks/{id} — return one task by id
@router.get("/{id}", response_model=schemas.TaskResponse)
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        # Return 404 if task doesn't exist
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# PUT /tasks/{id} — update an existing task
@router.put("/{id}", response_model=schemas.TaskResponse)
def update_task(id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Loop through updated fields and apply them to the existing task
    for key, value in task.model_dump().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

# DELETE /tasks/{id} — delete a task
@router.delete("/{id}")
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}