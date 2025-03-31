from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from HomeWork.app.backend.db_depends import get_db
from typing import Annotated
from HomeWork.app.models.task import Task
from HomeWork.app.models.user import User
from HomeWork.app.schemas import CreateUser, UpdateUser, CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router = APIRouter(prefix="/task", tags=["task"])


# Главная
@router.get("/")
async def all_task(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


# Информация
@router.get("/{task_id}")
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    return task


# Добавление
@router.post("/create")
async def create_task(create_tasks: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")

    new_task = Task(
        priority=0,
        user_id=user_id,
        content=create_tasks.content,
        title=create_tasks.title,
        completed=False,
        slug=slugify(create_tasks.title)
    )

    db.add(new_task)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


# Изменение
@router.put("/update")
async def update_task(task_id: int, updated_task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    query = select(Task).where(Task.id == task_id)
    task = db.scalar(query)
    if task:
        db.execute(update(User).where(Task.id == task_id).values(**updated_task.dict()))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "Task update is successful!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")


# Удаление
@router.delete("/delete")
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    query = select(User).where(Task.id == task_id)
    task = db.scalar(query)
    if task:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "Task deletion successful!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UTask was not found")