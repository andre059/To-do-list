from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///todo_list.db", echo=True)

SessionLocal = sessionmaker(bind=engine)
