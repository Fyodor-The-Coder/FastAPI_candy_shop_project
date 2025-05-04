from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from sqlalchemy import Column, JSON


class ProductBase(SQLModel):
    name: str = Field(max_length=100, index=True)
    description: Optional[str] = Field(max_length=300)
    price: float = Field(gt=0)
    category: str = Field(max_length=50)
    ingredients: List[str] = Field(
        sa_column=Column(JSON),
        min_items=3,
        max_items=4
    )
    stock: int = Field(default=0, ge=0)


class Product(ProductBase, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)

    order_items: List["OrderItem"] = Relationship(back_populates="product")
