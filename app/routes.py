from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from base import async_get_db
from .models import TodoItem
from .services import TodoService
from .schemas import TodoItemCreate, TodoItemUpdate

router = APIRouter()


@router.post("/api/todo", response_model=TodoItem)
async def create_todo(todo: TodoItemCreate, db: AsyncSession = Depends(async_get_db)):
    return await TodoService().create(todo, db)


@router.get("/api/todo/{id}", response_model=TodoItem)
async def read_todo(id: int, db: AsyncSession = Depends(async_get_db)):
    todo = await TodoService().get_by_id(id, db)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/api/todo/{id}", response_model=TodoItem)
async def update_todo(id: int, todo: TodoItemUpdate, db: AsyncSession = Depends(async_get_db)):
    return await TodoService().update(id, todo, db)


@router.delete("/api/todo/{id}")
async def delete_todo(id: int, db: AsyncSession = Depends(async_get_db)):
    await TodoService().delete(id, db)
    return {"message": "Todo deleted successfully"}
