from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import TodoItem
from .schemas import TodoItemCreate, TodoItemUpdate


class TodoService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(TodoItem).all()

    def get_by_id(self, id: int):
        return self.db.query(TodoItem).filter(TodoItem.id == id).first()

    def create(self, todo: TodoItemCreate):
        new_todo = TodoItem(**todo.dict())
        self.db.add(new_todo)
        self.db.commit()
        self.db.refresh(new_todo)
        return {"id": new_todo.id, "title": new_todo.title, "is_completed": new_todo.is_completed}

    def update(self, id: int, todo: TodoItemUpdate):
        existing_todo = self.get_by_id(id)
        if not existing_todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        for key, value in todo.dict().items():
            setattr(existing_todo, key, value)

        self.db.commit()
        self.db.refresh(existing_todo)
        return {"id": existing_todo.id, "title": existing_todo.title, "is_completed": existing_todo.is_completed}

    def delete(self, id: int):
        todo = self.get_by_id(id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        self.db.delete(todo)
        self.db.commit()
