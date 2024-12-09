from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from base import get_db
from .models import TodoItemResponse
from .services import TodoService
from .schemas import TodoItemCreate, TodoItemUpdate

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> TodoService:
    return TodoService(db)


@router.post("/api/todo", response_model=TodoItemResponse)
def create_todo(todo: TodoItemCreate, db: Session = Depends(get_service)):
    return TodoService(db).create(todo)


@router.get("/api/todo/{id}", response_model=TodoItemResponse)
def read_todo(id: int, db: Session = Depends(get_service)):
    todo = TodoService(db).get_by_id(id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/api/todo/{id}", response_model=TodoItemResponse)
def update_todo(id: int, todo: TodoItemUpdate, db: Session = Depends(get_service)):
    return TodoService(db).update(id, todo)


@router.delete("/api/todo/{id}")
def delete_todo(id: int, db: Session = Depends(get_service)):
    TodoService(db).delete(id)
    return {"message": "Todo deleted successfully"}
