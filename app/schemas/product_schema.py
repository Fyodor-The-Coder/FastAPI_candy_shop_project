from typing import List
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., example="Шоколадный торт")
    description: str | None = Field(
        default=None,
        example="Нежный шоколадный торт с ягодной прослойкой"
    )
    price: float = Field(..., example=1200.50, gt=0)
    category: str = Field(..., example="Торты")
    ingredients: List[str] = Field(
        ...,
        example=["мука", "сахар", "какао", "яйца"],
        min_length=3,
        max_length=4
    )
    stock: int = Field(..., example=10, ge=0)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int = Field(..., example=1)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [{
                "id": 1,
                "name": "Шоколадный торт",
                "price": 1200.50,
                "category": "Торты",
                "ingredients": ["мука", "сахар", "какао", "яйца"],
                "stock": 10
            }]
        }
