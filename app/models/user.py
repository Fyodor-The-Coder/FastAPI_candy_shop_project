"""
Модуль определения моделей пользователя системы.
Содержит SQLModel-классы для работы с данными пользователей в БД и валидации входных данных
"""
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class UserBase(SQLModel):
    """Базовая схема пользователя, содержащая общие атрибуты"""
    username: str = Field(index=True)
    email: str = Field(unique=True, index=True)


class User(UserBase, table=True):
    """Модель таблицы пользователей в базе данных"""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    orders: List["Order"] = Relationship(back_populates="user")
