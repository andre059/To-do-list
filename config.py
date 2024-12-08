from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

# Название SQLite базы данных
SQLITE_DB_NAME = "database.bd.db"

# URL для подключения к SQLite базе данных
SQLITE_URL = f"sqlite+aiosqlite:///C:\\Users\\aa\\{SQLITE_DB_NAME}"

# Параметры соединения
CONNECT_ARGS = {
    "check_same_thread": False  # Для поддержки многопоточность FastAPI
}

# Создаем движок SQLAlchemy
engine = create_async_engine(SQLITE_URL, connect_args=CONNECT_ARGS)

# Создаем SessionLocal для работы с базой данных
SessionLocal = sessionmaker(engine, expire_on_commit=False)
