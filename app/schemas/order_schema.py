from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = []


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_name: str
    price: float


class OrderResponse(BaseModel):
    id: int
    status: str
    user_id: int
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
