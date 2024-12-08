from pydantic import BaseModel


class TodoItemBase(BaseModel):
    title: str
    is_completed: bool | None = False


class TodoItemCreate(TodoItemBase):
    pass


class TodoItemUpdate(TodoItemBase):
    title: str | None
    is_completed: bool | None
