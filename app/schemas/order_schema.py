"""
Модуль со схемами валидации заказов
"""

from typing import List
from datetime import datetime
from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    """Модель для создания элементов заказа"""
    # pylint: disable=too-few-public-methods
    product_id: int
    quantity: int

    class Config:
        """
        Класс, необходимый для совместимости с ORM
        """
        from_attributes = True


class OrderCreate(BaseModel):
    """Модель создания нового заказа"""
    items: List[OrderItemCreate] = []


class OrderItemResponse(BaseModel):
    """
    Модель представления элемента заказа.
    Используется в ответах API для отображения деталей позиции заказа
    """
    id: int
    product_id: int
    quantity: int
    product_name: str
    price: float


class OrderResponse(BaseModel):
    """
    Полная модель представления заказа. Необходима для отображения детальной информации о заказе
    """
    # pylint: disable=too-few-public-methods
    id: int
    status: str
    user_id: int
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        """
        Класс, необходимый для совместимости с ORM
        """
        from_attributes = True
