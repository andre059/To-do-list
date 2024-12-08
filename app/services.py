from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import TodoItem
from .schemas import TodoItemCreate, TodoItemUpdate


class TodoService:
    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(TodoItem))
        return result.scalars().all()

    async def get_by_id(self, id: int, db: AsyncSession):
        result = await db.execute(select(TodoItem).filter(TodoItem.id == id))
        return result.scalars().first()

    async def create(self, todo: TodoItemCreate, db: AsyncSession):
        new_todo = TodoItem(**todo.dict())
        db.add(new_todo)
        await db.commit()
        await db.refresh(new_todo)
        return new_todo

    async def update(self, id: int, todo: TodoItemUpdate, db: AsyncSession):
        existing_todo = await self.get_by_id(id, db)
        if not existing_todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        for key, value in todo.dict().items():
            setattr(existing_todo, key, value)

        await db.commit()
        await db.refresh(existing_todo)
        return existing_todo

    async def delete(self, id: int, db: AsyncSession):
        todo = await self.get_by_id(id, db)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        await db.delete(todo)
        await db.commit()
