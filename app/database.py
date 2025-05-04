"""
Модуль для работы с базой данных SQLite с использованием SQLModel.
Содержит настройки подключения, сессии и утилиты для создания структуры БД
"""
from sqlmodel import create_engine, Session, SQLModel

SQLALCHEMY_DATABASE_URL = "sqlite:///./candy_shop.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True
)

def get_db():
    """Генератор сессий базы данных"""
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Инициализация структуры базы данных на основе SQLModel-классов"""
    SQLModel.metadata.create_all(engine)
