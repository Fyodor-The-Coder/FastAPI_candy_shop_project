"""
Модуль определения моделей заказов и позиций заказов.
Содержит SQLModel-классы для работы с системой заказов электронной коммерции
"""
from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func


class OrderItemBase(SQLModel):
    """Базовая схема позиции в заказе"""
    order_id: int = Field(foreign_key="orders.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int = Field(default=1, ge=1)


class OrderItem(OrderItemBase, table=True):
    """Модель таблицы позиций заказов в БД"""
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
        """Возвращает название товара из связанной записи Product"""
        return self.product.name if self.product else None

    @property
    def price(self):
        """Возвращает актуальную цену товара из связанной записи Product"""
        return self.product.price if self.product else None

class OrderBase(SQLModel):
    """Базовая схема заказа"""
    status: str = Field(default="created", max_length=20)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),  # pylint: disable=not-callable,
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
    """Модель таблицы заказов в БД"""
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
