import json
import logging
import asyncio

from fastapi import FastAPI, Depends, Request, Response
from sqlalchemy.orm import Session

from app.services import TodoService
from base import async_get_db, create_db_and_tables

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.middleware("startup")
async def startup():
    await asyncio.run(create_db_and_tables())


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        logger.debug("Attempting to get database session")
        db = next(async_get_db())
        logger.debug("Got database session")
        async with db:
            logger.debug("Entering async block")
            response = await call_next(request)
            logger.debug("Response received")
            return response
    except Exception as e:
        logger.error(f"Error in middleware: {str(e)}")
        return Response(content=json.dumps({"error": "Database error"}), status_code=500)


@app.get("/", response_model=dict)
async def root(todo_service: TodoService = Depends()):
    return {"message": "Welcome to ToDo List API!"}


# Для асинхронных операций используйте:
@app.get("/async")
async def async_root(db: Session = Depends(async_get_db)):
    return {"message": "Async operation successful"}
