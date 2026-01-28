"""
Task routes for creating, reading, updating, and deleting tasks.
"""
from fastapi import APIRouter,Depends,HTTPException,Response,status
from typing import List
from sqlalchemy.orm import Session
from api.deps import get_db
import schemas.task as task_schema
from models.task import Task
from sqlalchemy import func 

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=task_schema.TaskCreate, status_code=status.HTTP_201_CREATED)
def create_task(
    task: task_schema.TaskCreate,
    db: Session = Depends(get_db),   
) -> task_schema.TaskCreate:
    """
    Create a new task.

    param task: TaskCreate schema object\n
    param db: Database session\n
    return: Created Task object\n

    """
    try:
        db_task = Task(
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date,
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create task") from e

@router.get("/", response_model=List[task_schema.TaskBase], status_code=status.HTTP_200_OK)
def read_tasks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    search: str | None = None,
    filter_status: task_schema.StatusEnum | None = None,
    filter_priority: task_schema.PriorityEnum | None = None,
 ) -> List[task_schema.TaskBase]:
    """
    Retrieve a list of tasks with optional search and filtering.\n
    param skip: Number of records to skip for pagination\n
    param limit: Maximum number of records to return\n
    param db: Database session\n
    param search: Search term to filter tasks by title or description\n
    param filter_status: Filter tasks by status\n
    param filter_priority: Filter tasks by priority\n
    return: List of Task objects\n 
    """
    try:
        if search:
            tasks_query = db.query(Task).filter(Task.title.contains(search) | Task.description.contains(search)).where(Task.is_deleted == False)
        else:
            tasks_query = db.query(Task).where(Task.is_deleted == False)
        if filter_status:
            tasks_query = tasks_query.filter(Task.status == filter_status).where(Task.is_deleted == False)
        if filter_priority:
            tasks_query = tasks_query.filter(Task.priority == filter_priority).where(Task.is_deleted == False)
        tasks = tasks_query.offset(skip).limit(limit).all()
        return tasks
    except Exception as e:
       
        raise HTTPException(status_code=500, detail="Failed to retrieve tasks ") from e

@router.get("/{task_id}", response_model=task_schema.TaskBase, status_code=status.HTTP_200_OK)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a task by ID.

    param task_id: ID of the task to retrieve\n 
    param db: Database session\n
    return: Task object\n
    """
    try:
        task = db.query(Task).filter(Task.id == task_id).where(Task.is_deleted == False).first()
        if not task:
            return Response(status_code=404, media_type="application/json", content='{"detail":"Task not found"}')
        return task
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to retrieve task") from e
@router.put("/{task_id}", response_model=task_schema.TaskBase, status_code=status.HTTP_200_OK)
def update_task(
    task_id: int,
    task_update: task_schema.TaskUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a task by ID.
    
    param task_id: ID of the task to update\n
    param task_update: TaskUpdate schema object with updated fields\n
    param db: Database session\n
    return: Updated Task object\n
    """
    try:
        task = db.query(Task).filter(Task.id == task_id).where(Task.is_deleted == False).first()
        if not task:
            return  Response(status_code=404, media_type="application/json", content='{"detail":"Task not found"}')
        for var, value in vars(task_update).items():
            setattr(task, var, value) if value else None
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update task") from e


@router.patch("/{task_id}/priority", response_model=task_schema.TaskBase, status_code=status.HTTP_200_OK)
def update_task_priority(
    task_id: int,
    priority_update: task_schema.TaskPriporityUpdate,
    db: Session = Depends(get_db),
):
    """
    Update the priority of a task by ID.

    param task_id: ID of the task to update\n
    param priority_update: TaskPriporityUpdate schema object with new priority\n
    param db: Database\n
    return: Updated Task object\n
    """
    try:
        task = db.query(Task).filter(Task.id == task_id).where(Task.is_deleted == False).first()
        if not task:
            return Response(status_code=404, media_type="application/json", content='{"detail":"Task not found"}')
        task.priority = priority_update.priority
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update task priority") from e
@router.patch("/{task_id}/status", response_model=task_schema.TaskBase, status_code=status.HTTP_200_OK)
def update_task_status(
    task_id: int,
    status_update: task_schema.TaskStatusUpdate,
    db: Session = Depends(get_db),
):
    """
    Update the status of a task by ID.

    param task_id: ID of the task to update\n
    param status_update: TaskStatusUpdate schema object with new status\n
    param db: Database session\n
    return: Updated Task object\n
    """
    try:
        task = db.query(Task).filter(Task.id == task_id).where(Task.is_deleted == False).first()
        if not task:
            return Response(status_code=404, media_type="application/json", content='{"detail":"Task not found"}')
        task.status = status_update.status
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update task status") from e

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    """
    Soft delete a task by ID.

    param task_id: ID of the task to delete\n
    param db: Database session\n
    return: No content response\n
    """
    try:
        task = db.query(Task).filter(Task.id == task_id).where(Task.is_deleted == False).first()
        if not task:
            return Response(status_code=404, media_type="application/json", content='{"detail":"Task not found"}')
        task.is_deleted = True
        task.deleted_at =  func.now()
        db.commit()
        db.refresh(task)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete task") from e

