from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class TodoItem(Base):
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default="NOW()")

    def __repr__(self):
        return f"<TodoItem(id={self.id}, title='{self.title}', is_completed={self.is_completed})>"
