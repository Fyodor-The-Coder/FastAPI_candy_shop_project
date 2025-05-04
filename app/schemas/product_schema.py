from typing import List, Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: float
    category: str
    ingredients: List[str]
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    category: Optional[str]
    ingredients: Optional[List[str]]
    stock: Optional[int]

class ProductResponse(ProductBase):
    id: int

    class Config:
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
    id: int
    name: str
    price: float
    stock: int

    class Config:
        from_attributes = True
