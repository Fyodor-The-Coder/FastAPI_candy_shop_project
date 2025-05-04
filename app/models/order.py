from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, Integer, ForeignKey
from typing import List, Optional
from sqlalchemy.sql import func
from datetime import datetime


class OrderItemBase(SQLModel):
    order_id: int = Field(foreign_key="orders.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int = Field(default=1, ge=1)


class OrderItem(OrderItemBase, table=True):
    __tablename__ = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)

    product_id: int = Field(
        sa_column=Column(Integer, ForeignKey("products.id"))
    )
    order_id: int = Field(
        sa_column=Column(Integer, ForeignKey("orders.id"))
    )

    product: "Product" = Relationship(back_populates="order_items")
    order: "Order" = Relationship(back_populates="items")

    @property
    def product_name(self):
        return self.product.name if self.product else None

    @property
    def price(self):
        return self.product.price if self.product else None

class OrderBase(SQLModel):
    status: str = Field(default="created", max_length=20)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            name="created_at"
        )
    )

    user_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("users.id", name="fk_order_user_id")
        )
    )


class Order(OrderBase, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("users.id", name="fk_order_user_id")
        )
    )

    items: List[OrderItem] = Relationship(back_populates="order")
    user: "User" = Relationship(back_populates="orders")
