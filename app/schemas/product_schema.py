"""Модуль со схемами данных для работы с продуктами"""
from typing import List, Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    """
    Базовая модель данных продукта. Используется как родительский класс для других схем
    """
    name: str
    description: Optional[str]
    price: float
    category: str
    ingredients: List[str]
    stock: int

class ProductCreate(ProductBase):
    """
    Модель для создания нового продукта. Наследует все поля от ProductBase.
    Используется как входная схема для эндпоинтов создания продукта
    """

class ProductUpdate(BaseModel):
    """
    Модель для обновления данных продукта.
    Позволяет делать частичные обновления через PATCH-запросы.
    """
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    category: Optional[str]
    ingredients: Optional[List[str]]
    stock: Optional[int]

class ProductResponse(ProductBase):
    """
    Полная модель ответа с данными продукта
    """
    # pylint: disable=too-few-public-methods
    id: int

    class Config:
        """
        Класс, необходимый для совместимости с ORM.
        Также содержит пример данных для документации OpenAPI
        """
        from_attributes = True
        json_schema_extra = {
            "examples": [{
                "id": 1,
                "name": "Шоколадный торт",
                "description": "Нежный шоколадный торт с ягодной прослойкой",
                "price": 1200.50,
                "category": "Торты",
                "ingredients": ["мука", "сахар", "какао", "яйца"],
                "stock": 10
            }]
        }

class ProductShortInfo(BaseModel):
    """
    Модель краткой информации о продукте для списков и превью
    """
    # pylint: disable=too-few-public-methods
    id: int
    name: str
    price: float
    stock: int

    class Config:
        """
        Класс, необходимый для совместимости с ORM
        """
        from_attributes = True
