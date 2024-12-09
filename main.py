import json
import logging
from typing import Any

from fastapi import FastAPI, Depends, Request, Response
from sqlalchemy.orm import Session

from app.middleware import log_requests
from app.models import Base, TodoItemResponse
from app.routes import get_service
from base import get_db
from config import engine

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()


app.middleware("http")(log_requests)


@app.post("/setup")
def setup_database():
    with engine.connect() as connection:
        Base.metadata.drop_all(connection)
        Base.metadata.create_all(connection)
    return {"ok": "Database setup successful"}


@app.middleware("http")
def db_session_middleware(request: Request, call_next):
    try:
        logger.debug("Attempting to get database session")
        db = next(get_db())
        logger.debug("Got database session")
        with db:
            logger.debug("Entering async block")
            response = call_next(request)
            logger.debug("Response received")
            return response
    except Exception as e:
        logger.error(f"Error in middleware: {str(e)}")
        return Response(content=json.dumps({"error": "Database error"}), status_code=500)


@app.get("/", response_model=TodoItemResponse)
def root(todo_service: Any = Depends()):
    return {"message": "Welcome to ToDo List API!"}


@app.get("/sync")
def sync_root(db: Session = Depends(get_service)):
    return {"message": "Sync operation successful"}
