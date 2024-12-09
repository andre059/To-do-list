from pydantic import BaseModel, Field
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TodoItem(Base):
    __tablename__ = "todo_list"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = Field(..., max_length=100)
    is_completed: Mapped[bool] = Field(default=False)
    created_at: Mapped[datetime] = Field(default_factory=datetime.utcnow)


class TodoItemResponse(BaseModel):
    id: int
    title: str
    is_completed: bool
    created_at: datetime
