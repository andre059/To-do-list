from sqlmodel import SQLModel

from config import SessionLocal, engine


async def async_get_db():
    async with SessionLocal() as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# def get_db():
#     with SessionLocal() as session:
#         yield session
