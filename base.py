from fastapi import Depends
from sqlalchemy.ext.declarative import declarative_base

from config import SessionLocal

Base = declarative_base()


def get_db():
    with SessionLocal() as session:
        yield session


SessionDep = Depends(get_db)
