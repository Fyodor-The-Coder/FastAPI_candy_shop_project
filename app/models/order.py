from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, func


class OrderBase(SQLModel):
    user_id: int = Field(foreign_key="users.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int = Field(default=1, ge=1)
    status: str = Field(default="created", max_length=20)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True),
                         default=func.now()
                         ))

class Order(OrderBase, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)

    user: "User" = Relationship(back_populates="orders")
    product: "Product" = Relationship(back_populates="orders")
