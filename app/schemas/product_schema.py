from typing import List, Optional
from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str = Field(..., example="Шоколадный торт")
    description: Optional[str] = Field(
        default=None,
        example="Нежный шоколадный торт с ягодной прослойкой"
    )
    price: float = Field(..., example=1200.50, gt=0)
    category: str = Field(..., example="Торты")
    ingredients: List[str] = Field(
        ...,
        example=["мука", "сахар", "какао", "яйца"],
        min_length=3
    )
    stock: int = Field(..., example=10, ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Новый шоколадный торт")
    description: Optional[str] = Field(
        None,
        example="Обновленный рецепт с вишней"
    )
    price: Optional[float] = Field(None, example=1500.0, gt=0)
    category: Optional[str] = Field(None, example="Торты")
    ingredients: Optional[List[str]] = Field(
        None,
        example=["мука", "сахар", "какао", "вишня"],
        min_length=3
    )
    stock: Optional[int] = Field(None, example=15, ge=0)

class ProductResponse(ProductBase):
    id: int = Field(..., example=1)

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
