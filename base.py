from fastapi import Depends
from sqlalchemy.ext.declarative import declarative_base

from config import SessionLocal

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Depends(get_db)
